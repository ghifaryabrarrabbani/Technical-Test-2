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

select AVG(ser_time) as Average_Time from crmcallcenterlogs cc
join crmevents ce on cc.complaint_id = ce.complaint_id
where cc.ser_time is not null;

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

select ce.product, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by product;

select date_trunc('year', cc.date_received) as year_complaint, ce.sub_product,
cast(extract(epoch from avg(ser_time))as int) as Average_Time
from crmcallcenterlogs cc
join crmevents ce on cc.complaint_id = ce.complaint_id
where cc.complaint_id is not null and sub_product is not null
group by date_trunc('year', cc.date_received), ce.sub_product
order by year_complaint;

select ce.sub_product, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by sub_product;

select date_trunc('year', cc.date_received) as year_complaint, ce.timely_response, ce.consumer_disputed,
cast(extract(epoch from avg(ser_time))as int) as Average_Time
from crmcallcenterlogs cc
join crmevents ce on cc.complaint_id = ce.complaint_id
where cc.complaint_id is not null and ce.consumer_disputed is not null
group by date_trunc('year', cc.date_received), ce.timely_response, ce.consumer_disputed
order by year_complaint;

select ce.timely_response, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by ce.timely_response;

select ce.consumer_disputed, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by ce.consumer_disputed;

select cc.server_, cast(extract(epoch from avg(ser_time))as int) as Average_Time, count(*) as total_customer
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by cc.server_
order by cast(extract(epoch from avg(ser_time))as int) desc
limit  5;

select cc.server_, cast(extract(epoch from avg(ser_time))as int) as Average_Time, count(*) as total_customer
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
group by cc.server_
order by cast(extract(epoch from avg(ser_time))as int) asc
limit  5;

select cc.server_, count(*)
from crmevents ce
join crmcallcenterlogs cc on ce.complaint_id = cc.complaint_id
where ce.timely_response = 'No'
group by cc.server_
having count(*) > 2
