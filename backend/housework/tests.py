from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch
from .models import Contributor, HouseworkRecord


class BaseTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.contributor = Contributor.objects.create(name="Test User")
        self.test_image = SimpleUploadedFile(
            name="test_image.jpg",
            content=b"fake-image-content",
            content_type="image/jpeg",
        )


class ContributorTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.list_create_url = reverse('contributor-list')
        self.detail_url = lambda pk: reverse('contributor-detail', args=[pk])

    def test_crud_operations(self):
        # Create
        response = self.client.post(
            self.list_create_url, {"name": "New User"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contributor.objects.count(), 2)

        # Read (list)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)

        # Read (detail)
        response = self.client.get(self.detail_url(self.contributor.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Test User")

        # Update
        response = self.client.put(
            self.detail_url(self.contributor.id),
            {"name": "Updated User"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contributor.refresh_from_db()
        self.assertEqual(self.contributor.name, "Updated User")

        # Delete
        response = self.client.delete(self.detail_url(self.contributor.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contributor.objects.count(), 1)


class HouseworkRecordTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.record = HouseworkRecord.objects.create(
            note="Test Task",
            points=10,
            contributor=self.contributor
        )
        self.list_create_url = reverse('houseworkrecord-list')
        self.detail_url = lambda pk: reverse('houseworkrecord-detail', args=[pk])

    def test_crud_operations(self):
        # Create
        data = {
            "contributor_name": "John Doe",
            "points": 3,
            "note": "Cleaned the kitchen"
        }
        response = self.client.post(self.list_create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["contributor"]["name"], "John Doe")

        # Read (list)
        response = self.client.get(self.list_create_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data['results']) >= 1)

        # Read (detail)
        response = self.client.get(self.detail_url(self.record.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['note'], "Test Task")

        # Update
        data = {
            "note": "Updated Task",
            "points": 15,
            "contributor_name": "Test User"
        }
        response = self.client.put(
            self.detail_url(self.record.id),
            data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["note"], "Updated Task")

        # Delete
        response = self.client.delete(self.detail_url(self.record.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @patch("housework.views.get_minio_client")
    def test_image_operations(self, mock_get_minio):
        mock_client = mock_get_minio.return_value
        mock_client.put_object.return_value = None
        
        # Create with image
        data = {
            "contributor_name": "Jane Doe",
            "points": 5,
            "note": "Vacuumed",
            "image": self.test_image
        }
        response = self.client.post(
            self.list_create_url,
            data,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("image" in response.data)
        self.assertTrue(mock_client.put_object.called)

        # Update with image
        new_image = SimpleUploadedFile(
            name="updated_image.jpg",
            content=b"new-fake-image-content",
            content_type="image/jpeg"
        )
        data["image"] = new_image
        data["note"] = "Updated task"
        response = self.client.put(
            self.detail_url(response.data['id']),
            data,
            format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("image" in response.data)

    def test_error_handling(self):
        # Test invalid record ID
        response = self.client.get(self.detail_url(999))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Test invalid data
        response = self.client.post(
            self.list_create_url,
            {"points": "invalid"},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
