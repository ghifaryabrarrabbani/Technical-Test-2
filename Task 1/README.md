# Average Serving Time Report 2011-2017
This project analyze of average serving time on 2011-2017 to determine the average serving time across several sectors to gain insights and identify improvement opportunities.

## Description
This project contains two dataset from https://drive.google.com/drive/folders/120NBGrMC7DSutH8C3Z5BgxqzRCzY0uA7, such as:
1. CRMEvents: Contains all complaint events from all channels.
2. CRMCallCenterLogs: Contains only complaints submitted via phone.

## Getting Started
### Dependencies
Ensure that ypu have the following installed and ready to use on your system:
- Docker Desktop
- pgAdmin

### How to Use
1. Open the terminal or powershell (make sure run it as administrator)
2. Type the following commmand: 
``` 
docker run --name <name_of_container> -e POSTGRES_PASSWORD=<passoword_of_container> -p <port>:5432 -d postgres
```
Make sure to input the name_of_container, password_of_container, and port. In my case, I use :
- name_of_container: Ghifary_Task_1
- passoword_of_container: mandiri123
- port: 5431
3. Check if the container has been made (you can check it on the docker desktop application or run this code)
``` 
docker ps -a
```
4. Open the pgadmin application to access PostgreSQL databases. Click on server in the left menu and register new server. There are several things that need to be provide, such as:
-  On General sub menu, input anything for the name of your database
- Move to the Connection sub menu, input: hostname as localhost, port as the same port you use (in my case, my port is 5431), and input passwrd as the same passwor d of the container (in my case, my password is mandiri123)
5. Create the tables by open the query tool and run this code
``` sql
CREATE TABLE CRMEvents (
Date_received DATE,
Product TEXT,
Sub_product TEXT,
Issue TEXT,
Sub_issue TEXT,
Consumer_complaint_narrative TEXT,
Tags TEXT,
Consumer_consent_provided TEXT,
Submitted_via TEXT,
Date_sent_to_company DATE,
Company_response_to_consumer TEXT,
Timely_response TEXT,
Consumer_disputed TEXT,
Complaint_ID TEXT,
Client_ID TEXT
);

CREATE TABLE crmcallcenterlogs (
Date_received DATE,        
Complaint_ID VARCHAR, 
rand_client VARCHAR,
phonefinal VARCHAR, 
vru_line VARCHAR,
call_id VARCHAR,
priority VARCHAR,   
type_ VARCHAR,
outcome VARCHAR,
server_ VARCHAR,
ser_start TIME,
ser_exit TIME, 
ser_time INTERVAL       
);
```
6. Import the data to the table by using the PSQL tool because the import was done using local and run this code
```
\copy crmevents FROM '<directory of file path to your csv file>' DELIMITER ',' CSV
HEADER QUOTE '"' ESCAPE '"'
```
```
\copy crmcallcenterlogs FROM '<directory of file path to your csv file>' DELIMITER ',' CSV HEADER QUOTE '"' ESCAPE '"
```
In my case, I'm using 'C:/Users/AGUNG TJAHJONO/Downloads/Ghifary Code/CRMCallCenterLogs.csv'
7. Since all of the process before do the analyze has been done, the next process will be run the code to gain insights.

- Total Complaints per Year
``` sql
select date_trunc('year', Date_received) as year,COUNT(*) AS complaints_per_year 
from crmevents
group by date_trunc('year', Date_received)
order by year;
```

- Total Complaints Based on Type of Submission
```sql 
select count(*) from crmevents
where submitted_via = 'Phone';

select count(*) from crmcallcenterlogs;

select distinct complaint_id, count(*) as total_calls
from crmcallcenterlogs
group by distinct complaint_id
having count(*) > 1
order by total_calls desc;
-- This analysis was also done manually by counting the total complaints submitted via phone from CRMEvents and comparing it with the total valid complaints in CRMCallCenterLogs (total minus null complaint IDs). The numbers matched, confirming data consistency.
```

- Average Serving Time
```sql 
select AVG(ser_time) as Average_Time from crmcallcenterlogs cc
join crmevents ce on cc.complaint_id = ce.complaint_id
where cc.ser_time is not null;
```
- Product as The Segment of Analysis Average Serving Time
```sql
select date_trunc('year', cc.date_received) as year_complaint, 
cast(extract(epoch from avg(ser_time))as int) as Average_Time
from crmcallcenterlogs cc
join crmevents ce on cc.complaint_id = ce.complaint_id
where ce.product = 'Bank account or service'
group by date_trunc('year', cc.date_received)
order by year_complaint;

select date_trunc('year', cc.date_received) as year_complaint, 
cast(extract(epoch from avg(ser_time))as int) as Average_Time
from crmcallcenterlogs cc
join crmevents ce on cc.complaint_id = ce.complaint_id
where ce.product = 'Credit card'
group by date_trunc('year', cc.date_received)
order by year_complaint;
```

- Total Complaints Based on Product
```sql
select ce.product, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by product;
```

- Sub Product as the segment of analysis average of serving time
```sql
select date_trunc('year', cc.date_received) as year_complaint, ce.sub_product,
cast(extract(epoch from avg(ser_time))as int) as Average_Time
from crmcallcenterlogs cc
join crmevents ce on cc.complaint_id = ce.complaint_id
where cc.complaint_id is not null and sub_product is not null
group by date_trunc('year', cc.date_received), ce.sub_product
order by year_complaint;
```

- Total Complaints Based on Sub Product
```sql
select ce.sub_product, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by sub_product;
```

- Average Serving Time based on Timely Response-Consumer Disputed Over The Years
```sql
select date_trunc('year', cc.date_received) as year_complaint, ce.timely_response, ce.consumer_disputed,
cast(extract(epoch from avg(ser_time))as int) as Average_Time
from crmcallcenterlogs cc
join crmevents ce on cc.complaint_id = ce.complaint_id
where cc.complaint_id is not null and ce.consumer_disputed is not null
group by date_trunc('year', cc.date_received), ce.timely_response, ce.consumer_disputed
order by year_complaint;
```

- Total Complaints Based on Timely Response
``` sql
select ce.timely_response, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by ce.timely_response;
```

- Total Complaints Based on Consumer Disputed
```sql
select ce.consumer_disputed, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by ce.consumer_disputed;
```

- Top 5 (Descending) of Average Time by Server
```sql
select cc.server_, cast(extract(epoch from avg(ser_time))as int) as Average_Time, count(*) as total_customer
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by cc.server_
order by cast(extract(epoch from avg(ser_time))as int) desc
limit  5;
```

- Top 5 (Ascending) of Average Time by Server
```sql
select cc.server_, cast(extract(epoch from avg(ser_time))as int) as Average_Time, count(*) as total_customer
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by cc.server_
order by cast(extract(epoch from avg(ser_time))as int) asc
limit  5;
```

- Servers > 2 Bad Timely Response
```sql
select cc.server_, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
where ce.timely_response = 'No'
group by cc.server_
having count(*) > 2
```

## Analysis
The analysis can be found on:
- Presentation: [https://github.com/ghifaryabrarrabbani/Technical-Test-2/blob/main/Task%201/Presentation_Task%201.pdf]
- Files: [http://github.com/ghifaryabrarrabbani/Technical-Test-2/tree/main/Task%201]

## Author
Created by Ghifary Abrar Rabbani Email: [ghifaryabrarrr@gmail.com]

Linkedin: [https://www.linkedin.com/in/ghifaryabrarrabbani/]

Github: [https://github.com/ghifaryabrarrabbani]
