import pandas as pd

data = pd.read_json("companies.json")
companies = data[["companyId", "companyName", "founded"]]
companies["founded"] = pd.to_datetime(companies["founded"])
companies.rename(columns = {"companyId": "company_id",
 							"companyName": "company_name"}, inplace = True)

c_ids = companies["company_id"]

addresses = pd.DataFrame(c_ids).join(pd.json_normalize(data["address"]))

employees = []

for id_, emps in zip(c_ids, data["employees"]):
	if type(emps) == list:
		for e in emps:
			e["company_id"] = id_
			employees.append(e)
 			
employees = pd.DataFrame(employees)
employees.rename(columns = {"employeeId": "employee_id"}, inplace = True)

contacts_list = employees.pop("contacts").to_list()
e_ids = employees["employee_id"]
contacts = []

for id_, emp_contacts in zip(e_ids, contacts_list):
	if type(emp_contacts) == list:
		for c in emp_contacts:
			c["employee_id"] = id_
			contacts.append(c)
 			
contacts = pd.DataFrame(contacts)
contacts.rename(columns = {"contactType": "contact_type",
 						   "contactId": "contact_id",
 						   "contactValue": "contact_value"}, inplace = True)

companies.to_csv("tables/companies.csv")
addresses.to_csv("tables/addresses.csv")
employees.to_csv("tables/employees.csv")
contacts.to_csv("tables/contacts.csv")

n_users = pd.unique(employees["employee_id"]).size
n_companies = pd.unique(companies["company_id"]).size
print(f"Number of users in the data:{n_users}")
print(f"Number of companies in the data:{n_companies}")
# other easier way after inspecting the companies.json file:
# 	~ cat companies.json | grep -E -o 'employeeId\"\:\".{36}\"' | uniq | wc -l
#	~ cat companies.json | grep -E -o 'companyId\"\:\".{36}\"' | uniq | wc -l


n_contacts = contacts.groupby("employee_id")["contact_id"].count()
n_contacts_bytype = contacts.groupby(["employee_id", "contact_type"])["contact_id"].count()
n_contacts.to_csv("tables/n_contacts.csv", header = ["count"])
n_contacts_bytype.to_csv("tables/n_contacts_bytype.csv", header = ["count"])
















