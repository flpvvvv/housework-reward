from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch, Mock
from .models import Contributor


class HouseworkRecordTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("add_housework_record")

    def test_create_housework_record_without_image(self):
        data = {
            "contributor_name": "John Doe",
            "points": 3,
            "note": "Cleaned the kitchen",
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["contributor"]["name"], "John Doe")
        self.assertEqual(response.data["points"], 3)

    def test_create_housework_record_invalid_data(self):
        data = {
            "points": "invalid",  # Points should be numeric
            "note": "Test note",  # Missing required contributor_name
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("housework.views.get_minio_client")
    def test_create_housework_record_with_image(self, mock_get_minio):
        # Mock MinIO client
        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_get_minio.return_value = mock_client

        # Create test image
        image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"fake-image-content",
            content_type="image/jpeg",
        )

        data = {
            "contributor_name": "Jane Doe",
            "points": 5,
            "note": "Vacuumed the house",
            "image": image,
        }

        response = self.client.post(self.url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["contributor"]["name"], "Jane Doe")
        self.assertEqual(response.data["points"], 5)
        self.assertTrue("image" in response.data)

        # Verify MinIO interactions
        mock_client.put_object.assert_called_once()


from rest_framework.test import APITestCase


class ContributorAPITests(APITestCase):
    def setUp(self):
        self.test_contributor = Contributor.objects.create(name="Test User")

    def test_can_create_contributor(self):
        url = reverse("add_contributor")
        data = {"name": "New User"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contributor.objects.count(), 2)
        self.assertEqual(Contributor.objects.get(name="New User").name, "New User")

    def test_can_update_contributor(self):
        url = reverse("update_contributor", args=[self.test_contributor.id])
        data = {"name": "Updated User"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_contributor.refresh_from_db()
        self.assertEqual(self.test_contributor.name, "Updated User")

    def test_can_delete_contributor(self):
        url = reverse("delete_contributor", args=[self.test_contributor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contributor.objects.count(), 0)

    def test_cannot_update_nonexistent_contributor(self):
        url = reverse("update_contributor", args=[999])
        data = {"name": "Updated User"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_nonexistent_contributor(self):
        url = reverse("delete_contributor", args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import HouseworkRecord, Contributor
from unittest.mock import patch
from django.core.files.uploadedfile import SimpleUploadedFile


class HouseworkRecordTests(APITestCase):
    def setUp(self):
        self.contributor = Contributor.objects.create(name="Test User")
        self.record = HouseworkRecord.objects.create(
            note="Test Task", points=10, contributor=self.contributor
        )
        self.test_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"fake-image-content",
            content_type="image/jpeg",
        )
        self.test_url = "http://test-url/image.jpg"  # Add this line for reuse

    @patch("housework.views.get_minio_client")
    def test_update_housework_record(self, mock_get_minio):
        mock_client = mock_get_minio.return_value
        mock_client.bucket_exists.return_value = True

        url = reverse("update_housework_record", args=[self.record.id])
        data = {
            "note": "Updated Task",
            "points": 15,
            "contributor_name": self.contributor.name,  # Changed from contributor ID to name
        }

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["note"], "Updated Task")
        self.assertEqual(response.data["points"], 15)

    @patch("housework.views.get_minio_client")
    def test_update_housework_record_with_image(self, mock_get_minio):
        # Configure mock MinIO client
        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_client.put_object.return_value = None
        # Use a fixed URL for testing
        test_url = "http://test-url/image.jpg"
        mock_client.generate_presigned_url.return_value = test_url
        mock_get_minio.return_value = mock_client

        url = reverse("update_housework_record", args=[self.record.id])
        data = {
            "note": "Updated Task",
            "points": 15,
            "contributor_name": self.contributor.name,
            "image": self.test_image,
        }

        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("image", response.data)
        self.assertEqual(response.data["image"], test_url)

    @patch("housework.views.get_minio_client")
    def test_update_record_keeps_existing_image(self, mock_get_minio):
        # Setup record with existing image
        self.record.image = self.test_url
        self.record.save()

        url = reverse("update_housework_record", args=[self.record.id])
        data = {
            "note": "Updated without changing image",
            "points": 15,
            "contributor_name": self.contributor.name,
        }

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["image"], self.test_url)  # Image URL should remain unchanged

    @patch("housework.views.get_minio_client")
    def test_update_record_add_new_image(self, mock_get_minio):
        # Setup record without image
        self.record.image = None
        self.record.save()

        # Configure mock MinIO client
        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_client.generate_presigned_url.return_value = self.test_url
        mock_get_minio.return_value = mock_client

        url = reverse("update_housework_record", args=[self.record.id])
        data = {
            "note": "Added new image",
            "points": 15,
            "contributor_name": self.contributor.name,
            "image": self.test_image,
        }

        response = self.client.put(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["image"], self.test_url)
        mock_client.put_object.assert_called_once()

    def test_update_housework_record_invalid_id(self):
        url = reverse("update_housework_record", args=[999])
        data = {
            "note": "Updated Task",
            "points": 15,
            "contributor": self.contributor.id,
        }

        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_housework_record(self):
        url = reverse("delete_housework_record", args=[self.record.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HouseworkRecord.objects.count(), 0)

    def test_delete_housework_record_invalid_id(self):
        url = reverse("delete_housework_record", args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class HouseworkTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.contributor = Contributor.objects.create(name="Alice")
        self.record = HouseworkRecord.objects.create(
            contributor=self.contributor,
            points=5,
            note="Initial record"
        )
        self.update_url = reverse('update_housework_record', args=[self.record.id])  # Fixed URL name

    def test_update_housework_record_new_contributor(self):
        # Prepare update data with a new contributor
        update_data = {
            'contributor_name': 'Bob',
            'points': 8,
            'note': 'Updated record'
        }

        # Perform update request
        response = self.client.put(self.update_url, update_data, format='json')

        # Check response status and data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['contributor']['name'], 'Bob')
        self.assertEqual(response.data['points'], 8)
        self.assertEqual(response.data['note'], 'Updated record')

        # Verify new contributor was created
        self.assertTrue(Contributor.objects.filter(name='Bob').exists())
        
        # Verify record was updated with new contributor
        updated_record = HouseworkRecord.objects.get(id=self.record.id)
        self.assertEqual(updated_record.contributor.name, 'Bob')
