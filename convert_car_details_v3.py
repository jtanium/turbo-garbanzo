import csv
import re

class CarV3Record:
    def __init__(self, row):
        self.make_model = row['name']
        self.model_year = row['year']
        self.price = row['selling_price']
        self.km_driven = row['km_driven']
        self.fuel = row['fuel']
        self.seller_type = row['seller_type']
        self.transmission = row['transmission']
        self.owner = row['owner']
        self.fuel_economy = row['mileage']
        self.engine_cc = row['engine']
        self.horsepower = row['max_power']
        self.torque = row["torque"]
        self.seats = row["seats"]

    def make(self):
        if self.make_model.startswith("Land Rover"):
            return "Land Rover"
        else:
            return self.make_model.split()[0]

    def make_model_key(self):
        return ("is %s %s" % (self.make().lower(), self.model().lower())).replace(" ", "_")

    def model(self):
        return self.make_model.replace(self.make(), "").split()[0]

    def trim(self):
        return self.make_model.replace(self.make() + " " + self.model() + " ", "")

    def fuel_type_key(self):
        return "is_%s" % self.fuel.lower()

    def seller_type_key(self):
        return "is_%s" % self.seller_type.lower().replace(" ", "_")

    def transmission_type_key(self):
        return "is_%s" % self.transmission.lower()

    def owner_key(self):
        if self.owner == "Fourth & Above Owner" or self.owner == "Test Drive Car":
            return "is_other_owner"
        else:
            return "is_%s" % self.owner.lower().replace(" ", "_")

    def fuel_economy_kmpl(self):
        return re.sub("[^0-9.]", "", self.fuel_economy)

    def engine_cc2(self):
        return re.sub("[^0-9.]", "", self.engine_cc)

    def to_h(self):
        return {self.make_model_key(): 1,
                self.fuel_type_key(): 1,
                self.seller_type_key(): 1,
                self.transmission_type_key(): 1,
                self.owner_key(): 1,
                "model_year": self.model_year,
                "km_driven": self.km_driven,
                "fuel_econ_kmpl": self.fuel_economy_kmpl(),
                "engine_cc": self.engine_cc2(),
                "seats": self.seats,
                "price": self.price}


make_model_keys = set()
records = []
with open("Car details v3.csv", newline="") as car_v3:
    reader = csv.DictReader(car_v3)
    for row in reader:
        record = CarV3Record(row)
        make_model_keys.add(record.make_model_key())
        records.append(record)


# print(makes)

output_fieldnames = []
sorted_makes = list(make_model_keys)
sorted_makes.sort()
for make in sorted_makes:
    output_fieldnames.append(make)

output_fieldnames.append("is_cng")
output_fieldnames.append("is_diesel")
output_fieldnames.append("is_lpg")
output_fieldnames.append("is_petrol")
output_fieldnames.append("is_automatic")
output_fieldnames.append("is_manual")
output_fieldnames.append("is_dealer")
output_fieldnames.append("is_individual")
output_fieldnames.append("is_trustmark_dealer")
output_fieldnames.append("is_first_owner")
output_fieldnames.append("is_second_owner")
output_fieldnames.append("is_third_owner")
output_fieldnames.append("is_other_owner")
output_fieldnames.append("model_year")
output_fieldnames.append("km_driven")
output_fieldnames.append("fuel_econ_kmpl")
output_fieldnames.append("engine_cc")
output_fieldnames.append("seats")
output_fieldnames.append("price")

print(output_fieldnames)


def new_default_record(fieldnames):
    result = {}
    for f in fieldnames:
        result[f] = 0
    return result


with open("car_details_v3.csv", 'w', newline="") as output:
    writer = csv.DictWriter(output, fieldnames=output_fieldnames)
    writer.writeheader()
    for record in records:
        if record.fuel_economy == "":
            continue
        out_record = new_default_record(output_fieldnames)
        out_record.update(record.to_h())
        writer.writerow(out_record)

