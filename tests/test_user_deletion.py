import unittest
from unittest.mock import patch

from core import auth, db
from templates.users import render_desk_users


class UserDeletionTests(unittest.TestCase):
    def setUp(self):
        self.store = {
            "users": [
                {"email": "admin@example.com", "full_name": "Admin", "role": "admin"},
                {"email": "other-admin@example.com", "full_name": "Other Admin", "role": "admin"},
                {"email": "staff@example.com", "full_name": "Staff", "role": "sales"},
            ]
        }

    def test_admin_deletes_account_and_records_activity(self):
        with patch.object(db, "_use_pg", return_value=False), \
                patch.object(db, "_load_data", return_value=self.store), \
                patch.object(db, "_save_data") as save_data, \
                patch.object(db, "log_activity") as log_activity:
            result = db.delete_user_account(" STAFF@example.com ", "admin@example.com")

        self.assertEqual(result, "deleted")
        self.assertNotIn("staff@example.com", [user["email"] for user in self.store["users"]])
        save_data.assert_called_once_with(self.store)
        log_activity.assert_called_once_with(
            "admin@example.com",
            "User Account Deleted",
            "Administrator deleted user account staff@example.com",
        )

    def test_self_and_last_admin_deletion_are_blocked(self):
        self.store["users"] = self.store["users"][:1]
        with patch.object(db, "_use_pg", return_value=False), \
                patch.object(db, "_load_data", return_value=self.store), \
                patch.object(db, "_save_data") as save_data, \
                patch.object(db, "log_activity") as log_activity:
            self.assertEqual(
                db.delete_user_account("ADMIN@example.com", "admin@example.com"),
                "self",
            )
            self.assertEqual(
                db.delete_user_account("admin@example.com", "other-admin@example.com"),
                "last_admin",
            )

        save_data.assert_not_called()
        log_activity.assert_not_called()
        self.assertEqual(len(self.store["users"]), 1)

    def test_admin_ui_only_offers_delete_for_other_accounts(self):
        admin = {"email": "admin@example.com", "full_name": "Admin", "role": "admin"}
        html = render_desk_users(admin, self.store["users"])
        self.assertEqual(html.count('action="/api/users/delete"'), 2)
        self.assertNotIn('value="admin@example.com"', html)

        staff_html = render_desk_users(
            {"email": "staff@example.com", "full_name": "Staff", "role": "sales"},
            self.store["users"],
        )
        self.assertNotIn("/api/users/delete", staff_html)

    def test_deleting_account_revokes_its_active_sessions(self):
        original_sessions = dict(auth.ACTIVE_SESSIONS)
        try:
            auth.ACTIVE_SESSIONS.clear()
            deleted_token = auth.create_session({"email": "staff@example.com"})
            retained_token = auth.create_session({"email": "admin@example.com"})

            auth.destroy_sessions_for_user(" STAFF@example.com ")

            self.assertIsNone(auth.get_session_user(deleted_token))
            self.assertIsNotNone(auth.get_session_user(retained_token))
        finally:
            auth.ACTIVE_SESSIONS.clear()
            auth.ACTIVE_SESSIONS.update(original_sessions)


if __name__ == "__main__":
    unittest.main()
