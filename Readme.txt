Admin Dashboard

Total collected, pending, overdue payments tracking
Real-time cash flow overview for bank and hand cash
Agent-wise collection tracking


Accountant Dashboard

Cash flow statements with the CashFlow model
Transaction logs and reconciliation
Report generation for monthly/weekly reports


Collection Agent Dashboard

Assigned customers tracking
Daily collection status
Transaction history

Notifications & Alerts

Payment due reminders via the PaymentSchedule model
Alerts for overdue payments and large transactions
Admin notifications for bank deposits and cash updates


Security & Access Control

Role-based access through the CustomUser model
Audit logs for every transaction and modification
Data backup and export capabilities via the Report model


-------------------------------------------------------------------------------------------------
Model Name	                                     Purpose / Use Case
__________________________________________________________________________________________________
CustomUser                	     Stores basic user details and authentication information.

Role	                         Defines different user roles such as Admin, Accountant, Collection Agent

Customer	                     Stores customer details, including contact and personal information

Scheme	                         Represents different cash collection schemes/plans available for customers

CustomerScheme                   Links a customer to a specific scheme they have enrolled in

Transaction	Records              financial transactions such as payments, deposits, and withdrawals

TransactionReconciliation	     Tracks and corrects discrepancies in transactions (ensures reconciliation)

CashCollection	                 Records cash collected by collection agents from customers

CollectionAgent	                 Stores details about collection agents who collect payments from customers

Accountant	                     Stores details about accountants who manage financial records

AdminDashboard                	 Provides analytics and reporting for administrators

AccountantDashboard	             Displays financial summaries and transaction reports for accountants

CollectionAgentDashboard	     Shows assigned collections and pending payments for collection agents

Notification	                 Manages system notifications for various events such as payment due, transaction status

AuditLog	                     Logs system changes for security, tracking actions like data modifications and reconciliations


>>git rm --cached -r */migrations/*
>> git add .
>> git commit -m "Removed all migration files except __init__.py"
>>git push origin production




for remove all the migration files

windows
--------
Get-ChildItem -Path . -Recurse -Filter "*.py" | Where-Object { $_.Name -ne "__init__.py" -and $_.FullName -match "migrations" } | Remove-Item -Force

linux
-----

find . -path "*/migrations/*.py" -not -name "__init__.py" -delete


aswrgtrhytujttdrstere
DATABASES NAMES 

IN PRODUCTION
cashcollectionpayprdn

IN DEVELOPMENT
cashcollectionpay