import pandas as pd

path = r".\data\jobs.csv"

new_jobs = [
    ["Senior AWS Cloud Engineer","Lead the design and operation of large AWS environments, mentor engineers and manage complex cloud migrations","AWS,Terraform,Linux,CloudFormation",7,"London/Hybrid",0],
    ["Junior Cloud Support Analyst","Monitor AWS services, respond to alerts and provide first line support for cloud infrastructure","AWS,CloudWatch,Linux,Support",1,"Remote",1],
    ["IT Support Engineer","Provide first and second line technical support, troubleshoot Windows devices and manage user accounts","Windows,Active Directory,Microsoft 365,Networking",2,"Kent/Hybrid",1],
    ["Senior Network Engineer","Design enterprise network infrastructure, manage routing and switching and lead network projects","Cisco,Networking,TCP/IP,Routing",7,"London",0],
    ["Cloud Operations Technician","Monitor cloud infrastructure, investigate incidents and maintain operational documentation","AWS,Monitoring,Linux,Troubleshooting",2,"Remote",1],
    ["Junior Systems Administrator","Maintain Windows servers, manage user accounts and assist with backup and monitoring tasks","Windows,Active Directory,Backup,Networking",1,"Kent",1],
    ["DevOps Engineer","Develop automated deployment pipelines and manage containerised workloads in AWS","AWS,Docker,Kubernetes,CI/CD",4,"Remote",1],
    ["Cybersecurity Analyst","Monitor security events, investigate alerts and support vulnerability management activities","Security,SIEM,Networking,Linux",3,"London/Hybrid",1],
    ["Technical Support Analyst","Resolve software and hardware incidents and provide remote technical assistance to employees","Helpdesk,Windows,Microsoft 365,Troubleshooting",2,"Remote",1],
    ["AWS Infrastructure Engineer","Build and maintain scalable AWS infrastructure using Terraform and automation","AWS,Terraform,Networking,Linux",3,"Remote",1],

    ["Restaurant Manager","Manage restaurant operations, staff rotas, customer service and stock control","Hospitality,Management,Customer Service",4,"Kent",0],
    ["Recruitment Consultant","Source candidates, manage client relationships and meet recruitment placement targets","Recruitment,Sales,Communication,CRM",2,"London",0],
    ["Senior Frontend Developer","Build complex web applications using React, TypeScript and modern JavaScript frameworks","React,TypeScript,JavaScript,HTML",5,"Remote",0],
    ["Payroll Administrator","Process monthly payroll, maintain employee records and resolve payroll queries","Payroll,Excel,Administration,Finance",2,"Kent",0],
    ["Project Manager","Manage large technology projects, budgets, stakeholders and delivery schedules","Project Management,Agile,Budgeting,Leadership",5,"London",0],
    ["Office Administrator","Provide administrative support, organise meetings and maintain company records","Administration,Microsoft Office,Organisation",2,"Kent",0],
    ["Warehouse Operative","Receive deliveries, pick customer orders and maintain stock within a busy warehouse","Warehouse,Stock Control,Logistics",1,"Kent",0],
    ["Social Media Specialist","Create social media content, manage online campaigns and analyse audience engagement","Social Media,Marketing,Content,Analytics",2,"Remote",0],
    ["Senior Python Developer","Design high-performance backend systems using Python, Django and distributed services","Python,Django,APIs,Software Development",6,"London",0],
    ["Account Manager","Manage customer accounts, develop commercial relationships and identify sales opportunities","Sales,Account Management,CRM,Communication",3,"London",0],
]

df = pd.read_csv(path)

columns = [
    "job_title",
    "description",
    "skills",
    "experience_required",
    "location",
    "match"
]

new_df = pd.DataFrame(new_jobs, columns=columns)

df = pd.concat([df, new_df], ignore_index=True)

df.to_csv(path, index=False)

print(f"Dataset now contains {len(df)} jobs.")
print()
print(df["match"].value_counts().sort_index())
