# main/tests.py (or main/tests/test_contact_submission_view.py)
from django.test import TestCase
from django.urls import reverse
from main.models import CbContactSubmission  # ensure this exists

class ContactSubmissionViewTest(TestCase):
    def test_post_to_index_creates_contact_submission(self):
        data = {
            "first_name": "Matthew",
            "last_name": "Mullins",
            "phone": "123-456",
            "email": "matthewmullins1219@gmail.com",
            "content": "Hello",
        }

        # Use the correct URL name for index ('home-page' per your urls.py)
        resp = self.client.post(reverse("home-page"), data)

        # Expect redirect to thank-you page
        self.assertEqual(resp.status_code, 302)
        # If you have the thank-you URL named 'contact-thank-you', assert it:
        # self.assertRedirects(resp, reverse("contact-thank-you"))

        # Verify a row was created
        self.assertTrue(
            CbContactSubmission.objects.filter(email="matthewmullins1219@gmail.com").exists(),
            "Expected a CbContactSubmission to be created by index POST.",
        )
