# Copyright 2022 ACC Cyfronet AGH-UST

# Licensed under the Apache License, Version 2.0,
# copy of the license is available in the LICENSE file;

from django.test import TestCase
from grantstorage.localmodels.user import *
from datetime import date


class TestAffiliation(TestCase):
    @staticmethod
    def create_affiliation_model(type, units, status, end):
        return Affiliation(type, units, status, end)

    def test_affiliation_model(self):
        type = "ACADEMIC_UNIT_EMPLOYEE"
        units = ["Uniwersytet Warszawski",
                 "Wydział Fizyki"]
        status = "ACTIVE"
        end = date(2023, 5, 12)
        model = self.create_affiliation_model(type, units, status, end)

        self.assertEqual(model.type, type)
        self.assertEqual(model.units, units)
        self.assertEqual(model.status, status)
        self.assertEqual(model.end, end)
        self.assertEqual(model.__str__(), f'Affiliation: {type} {units} {status} {end}')

    def test_affiliation_serializer_contains_expected_fields(self):
        data = {"type": "ACADEMIC_EMPLOYEE",
                "units": ["Akademia Górniczo-Hutnicza im. Stanisława Staszica w Krakowie",
                          "Akademickie Centrum Komputerowe Cyfronet AGH"],
                "status": "INACTIVE",
                "end": date(2024, 10, 10)}
        serializer = AffiliationSerializer(data)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"type", "units", "status", "end"})
        self.assertEqual(data["type"], "ACADEMIC_EMPLOYEE")
        self.assertEqual(data["units"], ["Akademia Górniczo-Hutnicza im. Stanisława Staszica w Krakowie",
                                         "Akademickie Centrum Komputerowe Cyfronet AGH"])
        self.assertEqual(data["status"], "INACTIVE")
        self.assertEqual(data["end"], "2024-10-10")

    def test_affiliation_serializer_from_model(self):
        type = "ACADEMIC_UNIT_EMPLOYEE"
        units = ["Uniwersytet Jagielloński",
                 "Wydział Matematyki i Informatyki"]
        status = "ACTIVE"
        end = date(2025, 5, 3)
        model = self.create_affiliation_model(type, units, status, end)
        serializer = AffiliationSerializer(model)
        data = serializer.data

        self.assertEqual(set(data.keys()), {"type", "units", "status", "end"})
        self.assertEqual(data["type"], "ACADEMIC_UNIT_EMPLOYEE")
        self.assertEqual(data["units"], ["Uniwersytet Jagielloński",
                                         "Wydział Matematyki i Informatyki"])
        self.assertEqual(data["status"], "ACTIVE")
        self.assertEqual(data["end"], "2025-05-03")

    def test_affiliation_serializer_update(self):
        data = {"type": "ACADEMIC_UNIT_EMPLOYEE",
                "units": ["Akademickie Centrum Komputerowe Cyfronet AGH"],
                "status": "INACTIVE",
                "end": date(2023, 12, 21)}
        serializer = AffiliationSerializer(data=data)
        self.assertEqual(serializer.is_valid(), True)
        affiliation = serializer.save()

        new_data = {"type": "ACADEMIC_EMPLOYEE",
                    "units": ["Akademia Górniczo-Hutnicza im. Stanisława Staszica w Krakowie",
                              "Wydział Informatyki, Elektroniki i Telekomunikacji"],
                    "status": "ACTIVE",
                    "end": date(2025, 6, 1)}
        new_model = serializer.update(instance=affiliation, validated_data=new_data)
        new_serializer = AffiliationSerializer(new_model)
        new_data = new_serializer.data

        self.assertEqual(set(new_data.keys()), {"type", "units", "status", "end"})
        self.assertEqual(new_data["type"], "ACADEMIC_EMPLOYEE")
        self.assertNotEqual(new_data["type"], "ACADEMIC_UNIT_EMPLOYEE")

        self.assertEqual(new_data["units"], ["Akademia Górniczo-Hutnicza im. Stanisława Staszica w Krakowie",
                                             "Wydział Informatyki, Elektroniki i Telekomunikacji"])
        self.assertNotEqual(new_data["units"], ["Akademickie Centrum Komputerowe Cyfronet AGH"])

        self.assertEqual(new_data["status"], "ACTIVE")
        self.assertNotEqual(new_data["status"], "INACTIVE")

        self.assertEqual(new_data["end"], "2025-06-01")
        self.assertNotEqual(new_data["end"], "2023-12-21")
