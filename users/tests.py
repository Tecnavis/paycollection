from django.test import TestCase
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
import uuid

User = get_user_model()

class CustomUserTests(TestCase):
    def test_create_user_with_same_contact_number(self):
        """Test that multiple users can have the same contact number"""
        contact = "9876543210"
        
        # Create first user
        user1 = User.objects.create_user(contact_number=contact, password="password123")
        self.assertEqual(user1.contact_number, contact)
        self.assertTrue(user1.username) # Should have a generated username
        
        # Create second user with SAME contact number
        user2 = User.objects.create_user(contact_number=contact, password="password456")
        self.assertEqual(user2.contact_number, contact)
        self.assertNotEqual(user1.username, user2.username) # Usernames must be different
        self.assertNotEqual(user1.id, user2.id)
        
        print(f"\nSUCCESS: Created two users with contact {contact}")
        print(f"User 1: {user1.username}")
        print(f"User 2: {user2.username}")

    def test_username_uniqueness(self):
        """Test that username is still unique"""
        contact = "1234567890"
        uid = uuid.uuid4()
        
        # Create user with explicit username
        User.objects.create_user(contact_number=contact, password="pw", username=f"user-{uid}")
        
        # Try to create another with SAME username (should fail)
        with self.assertRaises(IntegrityError):
            User.objects.create_user(contact_number="0987654321", password="pw", username=f"user-{uid}")
            
        print("\nSUCCESS: Username uniqueness is enforced")
