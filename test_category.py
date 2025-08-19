import unittest
from uuid import UUID
import uuid

from category import Category

class TestCategory(unittest.TestCase):
    def test_name_is_required(self):
        with self.assertRaisesRegex(TypeError, "missing 1 required positional argument: 'name'"):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with self.assertRaisesRegex(ValueError, "name must be less than 256 characters"):
            Category("a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category("Movie")
        self.assertEqual(type(category.id), UUID)

    def test_created_category_with_default_values(self):
        category = Category("Movie")
        self.assertEqual(category.name, "Movie")
        self.assertEqual(category.description, "")
        self.assertEqual(category.is_active, True)

    def test_category_is_created_as_active_by_default(self):
        category = Category("Movie")
        self.assertEqual(category.is_active, True)

    def test_category_is_created_with_provided_values(self):
        cat_id = uuid.uuid4()
        category = Category(
            id=cat_id,
            name="Movie",
            description="some description",
            is_active=False
        )
        self.assertEqual(category.id, cat_id)
        self.assertEqual(category.name, "Movie")
        self.assertEqual(category.description, "some description")
        self.assertEqual(category.is_active, False)

    def test_category_str_method(self):
        category = Category("Movie")
        self.assertEqual(str(category), "Category(name=Movie - description= (is_active=True))")

    def test_category_repr_method(self):
        category = Category("Movie")
        self.assertEqual(repr(category), "Category(name=Movie - description= (is_active=True))")

if __name__ == "__main__":
    unittest.main()