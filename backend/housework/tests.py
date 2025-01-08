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
        self.create_url = reverse("add_contributor")
        self.update_url = reverse("update_contributor", args=[self.contributor.id])
        self.delete_url = reverse("delete_contributor", args=[self.contributor.id])

    def test_crud_operations(self):
        # Create
        response = self.client.post(
            self.create_url, {"name": "New User"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contributor.objects.count(), 2)

        # Update
        response = self.client.put(
            self.update_url, {"name": "Updated User"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.contributor.refresh_from_db()
        self.assertEqual(self.contributor.name, "Updated User")

        # Delete
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contributor.objects.count(), 1)

    def test_error_handling(self):
        invalid_url = reverse("update_contributor", args=[999])
        response = self.client.put(invalid_url, {"name": "Updated User"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class HouseworkRecordTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.record = HouseworkRecord.objects.create(
            note="Test Task", points=10, contributor=self.contributor
        )
        self.create_url = reverse("add_housework_record")
        self.update_url = reverse("update_housework_record", args=[self.record.id])
        self.delete_url = reverse("delete_housework_record", args=[self.record.id])

    def test_create_record(self):
        data = {
            "contributor_name": "John Doe",
            "points": 3,
            "note": "Cleaned the kitchen",
        }
        response = self.client.post(self.create_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["contributor"]["name"], "John Doe")

        # Test invalid data
        response = self.client.post(
            self.create_url, {"points": "invalid"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("housework.views.get_minio_client")
    def test_image_operations(self, mock_get_minio):
        # Create with image
        data = {
            "contributor_name": "Jane Doe",
            "points": 5,
            "note": "Vacuumed",
            "image": self.test_image,
        }
        response = self.client.post(self.create_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue("image" in response.data)

        # Update with image
        data["note"] = "Updated task"
        response = self.client.put(self.update_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Update without changing image
        self.record.save()
        response = self.client.put(
            self.update_url,
            {
                "note": "No image change",
                "points": 15,
                "contributor_name": self.contributor.name,
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crud_operations(self):
        # Update
        data = {"note": "Updated Task", "points": 15, "contributor_name": "New User"}
        response = self.client.put(self.update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["note"], "Updated Task")

        # Delete
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(HouseworkRecord.objects.count(), 0)

    def test_error_handling(self):
        invalid_url = reverse("update_housework_record", args=[999])
        response = self.client.put(invalid_url, {"note": "Test"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        response = self.client.delete(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
