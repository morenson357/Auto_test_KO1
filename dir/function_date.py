dateContract = """
 SELECT
  Employees.DisplayString AS DisplayString,
  Contract.ContractSubject AS ContractSubject,
  Numbers.Number AS Number,
  CAST(DocumentMainInfo.RegDate AS DATE) AS DocumentMainInfoRegDate,
  Category.Name AS Categoryy,
  Counterparty.Name AS Counterpartyy,
  CONCAT(
  REPLACE(FORMAT(ROUND(Contract.ContractSum, 2), 'N2'), '.', ','),
  ' ',
  CASE
  WHEN Contract.ContractCurrency = 1 AND Contract.ContractSum IS NOT NULL THEN 'RUB'
  WHEN Contract.ContractCurrency = 0 AND Contract.ContractSum IS NOT NULL THEN 'EUR'
  WHEN Contract.ContractCurrency = 2 AND Contract.ContractSum IS NOT NULL THEN 'USD'
  END
  ) AS ContractSum,
  CAST(Contract.ContractBegin AS DATE) AS ContractBegin,
  CAST(Contract.ContractEnd AS DATE) AS ContractEnd,
  'http://vm-dv-report-01.corp.btlab.ru/DocsvisionWebClient/#/CardView/' + CAST(DocumentMainInfo.InstanceID AS NVARCHAR(MAX)) AS DocumentMainRowID,
  GETDATE() AS DateNow
 FROM
  [dvtable_{30eb9b87-822b-4753-9a50-a1825dca1b74}] AS DocumentMainInfo
  JOIN [dvtable_{3997861D-4FF5-496A-B8A2-D16617DE91D7}] AS Contract ON DocumentMainInfo.InstanceID = Contract.InstanceID
  JOIN [dvsys_instances] dvsys ON DocumentMainInfo.InstanceID = dvsys.InstanceID
  LEFT JOIN [Docsvision].[dbo].[dvtable_{DBC8AE9D-C1D2-4D5E-978B-339D22B32482}] AS Employees ON Employees.RowID = Contract.ContractResponsible
  JOIN [Docsvision].[dbo].[dvtable_{7473F07F-11ED-4762-9F1E-7FF10808DDD1}] AS Units ON Units.RowID = Employees.ParentRowID
  LEFT JOIN [Docsvision].[dbo].[dvtable_{CFDFE60A-21A8-4010-84E9-9D2DF348508C}] AS coll ON coll.RowID = Employees.Position
  LEFT JOIN [Docsvision].[dbo].[dvtable_{61C8CC7C-35CE-49E5-9CCD-E9F3C1129445}] AS Numbers ON Numbers.RowID = DocumentMainInfo.RegNumber
  LEFT JOIN [Docsvision].[dbo].[dvtable_{1B1A44FB-1FB1-4876-83AA-95AD38907E24}] AS Category ON Category.RowID = Contract.ContractGroup
  LEFT JOIN [Docsvision].[dbo].[dvtable_{C78ABDED-DB1C-4217-AE0D-51A400546923}] AS Counterparty ON Counterparty.RowID = Contract.PartnerCompany
 WHERE
  dvsys.Deleted = 0
  AND Contract.ContractSubject LIKE '%demo%'
  AND cond(StartDate, Contract.ContractEnd >= @StartDate)
  AND cond(EndDate, Contract.ContractEnd <= @EndDate)
  AND cond(StartContractSum, Contract.ContractSum >= @StartContractSum)
  AND cond(EndContractSum, Contract.ContractSum <= @EndContractSum)
  AND cond(ContractCurrency, Contract.ContractCurrency = @ContractCurrency)
  AND cond(PartnerPerson, Contract.ContractResponsible = @PartnerPerson)
  AND cond(Category, Contract.ContractGroup = @Category)
  AND cond(Subdivision, Employees.ParentRowID = @Subdivision)
 ORDER BY
  Employees.DisplayString,
  DocumentMainInfo.RegDate
 """

dateContractss = """
  SELECT
  Employees.DisplayString AS DisplayString,
  Units.Name AS Unit,
  coll.Name AS CollName,
  COUNT(Employees.DisplayString) AS CountEmployeesDisplay
 FROM
  [dvtable_{30eb9b87-822b-4753-9a50-a1825dca1b74}] AS DocumentMainInfo
  JOIN [dvtable_{3997861D-4FF5-496A-B8A2-D16617DE91D7}] AS Contract ON DocumentMainInfo.InstanceID = Contract.InstanceID
  JOIN [dvsys_instances] dvsys ON DocumentMainInfo.InstanceID = dvsys.InstanceID
  LEFT JOIN [Docsvision].[dbo].[dvtable_{DBC8AE9D-C1D2-4D5E-978B-339D22B32482}] AS Employees ON Employees.RowID = Contract.ContractResponsible
  JOIN [Docsvision].[dbo].[dvtable_{7473F07F-11ED-4762-9F1E-7FF10808DDD1}] AS Units ON Units.RowID = Employees.ParentRowID
  LEFT JOIN [Docsvision].[dbo].[dvtable_{CFDFE60A-21A8-4010-84E9-9D2DF348508C}] AS coll ON coll.RowID = Employees.Position
 WHERE
  dvsys.Deleted = 0
  AND Contract.ContractSubject LIKE '%demo%'
  AND cond(StartDate, Contract.ContractEnd >= @StartDate)
  AND cond(EndDate, Contract.ContractEnd <= @EndDate)
  AND cond(StartContractSum, Contract.ContractSum >= @StartContractSum)
  AND cond(EndContractSum, Contract.ContractSum <= @EndContractSum)
  AND cond(ContractCurrency, Contract.ContractCurrency = @ContractCurrency)
  AND cond(PartnerPerson, Contract.ContractResponsible = @PartnerPerson)
  AND cond(Category, Contract.ContractGroup = @Category)
  AND cond(Subdivision, Employees.ParentRowID = @Subdivision)
 GROUP BY
  Employees.DisplayString,
  coll.Name,
  Units.Name
"""
dateAdditionaloptions = "SELECT GETDATE() as DateNow"
