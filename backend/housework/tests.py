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
        self.url = reverse('add_housework_record')
        
    def test_create_housework_record_without_image(self):
        data = {
            'contributor_name': 'John Doe',
            'scale': 3,
            'note': 'Cleaned the kitchen'
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contributor']['name'], 'John Doe')
        self.assertEqual(response.data['scale'], 3)

    def test_create_housework_record_invalid_data(self):
        data = {
            'scale': 'invalid',  # Scale should be numeric
            'note': 'Test note'  # Missing required contributor_name
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch('housework.views.get_minio_client')
    def test_create_housework_record_with_image(self, mock_get_minio):
        # Mock MinIO client
        mock_client = Mock()
        mock_client.bucket_exists.return_value = True
        mock_get_minio.return_value = mock_client

        # Create test image
        image = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'fake-image-content',
            content_type='image/jpeg'
        )

        data = {
            'contributor_name': 'Jane Doe',
            'scale': 5,
            'note': 'Vacuumed the house',
            'image': image
        }
        
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['contributor']['name'], 'Jane Doe')
        self.assertEqual(response.data['scale'], 5)
        self.assertTrue('image' in response.data)
        
        # Verify MinIO interactions
        mock_client.put_object.assert_called_once()

from rest_framework.test import APITestCase

class ContributorAPITests(APITestCase):
    def setUp(self):
        self.test_contributor = Contributor.objects.create(
            name="Test User"
        )
        
    def test_can_create_contributor(self):
        url = reverse('add_contributor')
        data = {
            'name': 'New User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Contributor.objects.count(), 2)
        self.assertEqual(Contributor.objects.get(name='New User').name, 'New User')

    def test_can_update_contributor(self):
        url = reverse('update_contributor', args=[self.test_contributor.id])
        data = {
            'name': 'Updated User'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.test_contributor.refresh_from_db()
        self.assertEqual(self.test_contributor.name, 'Updated User')

    def test_can_delete_contributor(self):
        url = reverse('delete_contributor', args=[self.test_contributor.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Contributor.objects.count(), 0)

    def test_cannot_update_nonexistent_contributor(self):
        url = reverse('update_contributor', args=[999])
        data = {
            'name': 'Updated User'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_cannot_delete_nonexistent_contributor(self):
        url = reverse('delete_contributor', args=[999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
