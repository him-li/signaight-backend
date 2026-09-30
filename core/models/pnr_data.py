from datetime import date
from typing import Optional

from .base import SignAIghtSchema


class PNREmergencyContact(SignAIghtSchema):
    name: Optional[str] = None
    phone: Optional[str] = None


class PersonPNRData(SignAIghtSchema):
    passport_number: Optional[str] = None
    itinerary_profile: Optional[str] = None
    travel_frequency: Optional[str] = None
    emergency_contact: Optional[PNREmergencyContact] = None


class ProjectPNRData(SignAIghtSchema):
    departure_airport: Optional[str] = None
    arrival_airport: Optional[str] = None
    flight_date: Optional[date] = None
    airline: Optional[str] = None
    flight_number: Optional[str] = None
