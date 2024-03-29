# Generated by CodiumAI
from datetime import datetime

# Dependencies:
# pip install pytest-mock
import pytest
from pytest_mock import mocker
from sqlalchemy.exc import IntegrityError

from app.Exceptions.persistence_exceptions import RecordNotFoundException
from app.models import Odontogram
from app.services.odontogram_service import OdontogramService
from app.schemas.odontogram_schema import Odontogram as OdontogramSchema, OdontogramCreate


class TestOdontogramService:

    #  Tests that the method get_odontogram_by_id returns the correct Odontogram object when given a valid odontogram_id
    def test_get_odontogram_by_id(self, mocker):
        # Create a mock Odontogram object
        mock_odontogram = Odontogram(odontogram_id=1, patient_id=1, type_odontogram_id=1, details=[],
                                     created_at=datetime.now())

        # Create a mock Session object
        mock_session = mocker.Mock()
        mock_session.query.return_value.get.return_value = mock_odontogram

        # Create an instance of OdontogramService with the mock Session
        odontogram_service = OdontogramService(mock_session)

        # Call the get_odontogram_by_id method with a valid odontogram_id
        result = odontogram_service.get_odontogram_by_id(1)

        # Assert that the result is equal to the mock Odontogram object
        assert result == mock_odontogram

        # Assert that the query method of the mock Session object was called with the correct arguments
        mock_session.query.assert_called_once_with(Odontogram)

        # Assert that the get method of the mock query object was called with the correct argument
        mock_session.query.return_value.get.assert_called_once_with(1)

    #  Tests that the method get_detail_teeth handles an empty details list and returns an empty list of Tooth objects
    def test_get_detail_teeth_empty_details(self):
        # Create an empty list of DetailOdontogram objects
        details = []

        # Create an instance of OdontogramService
        odontogram_service = OdontogramService(None)

        # Call the get_detail_teeth method with the empty list of details
        result = odontogram_service.get_detail_teeth(details)

        # Assert that the result is an empty list
        assert result == []

    # Tests that the method create_odontogram raises a
    # RecordNotFoundException when the patient or type_odontogram do not exist
    def test_create_odontogram_record_not_found(self, mocker):
        # Create a mock OdontogramCreate object
        mock_odontogram_create = OdontogramCreate(patient_id=1, type_odontogram_id=1)

        # Create a mock Session object
        mock_session = mocker.Mock()
        mock_session.add.side_effect = IntegrityError(None, None, None)  # Correct way to raise IntegrityError

        # Create an instance of OdontogramService with the mock Session
        odontogram_service = OdontogramService(mock_session)

        # Call the create_odontogram method with the mock OdontogramCreate object
        with pytest.raises(RecordNotFoundException):
            odontogram_service.create_odontogram(mock_odontogram_create)

        # Assert that the add method of the mock Session object was called with the mock OdontogramCreate object
        mock_session.add.assert_called_once()

        # Assert that the commit method of the mock Session object was not called
        mock_session.commit.assert_not_called()

    #  Tests that the method get_detail_odontogram raises a RecordNotFoundException when the tooth is not found
    def test_get_detail_odontogram_tooth_not_found(self, mocker):
        # Create a mock Session object
        mock_session = mocker.Mock()
        mock_session.query.return_value

