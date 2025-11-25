# _This is a data miner and data visualiser for mendeley_

## Purpose:

The aim is to speed up research insights amongst me conducting a thorough thematic analysis, and back my claims via such tools like:

- Standardised frameworks
- Keyword frequencies 
- Frequency co-occurrences amongst reports
- Co-occurrence VOS connections between reports

---

The general flow:

1. extract mendeley collection using mendeley API & Collection .RIS export (for co-citation vos mapping)
2. Clean, normalise and filter the data using PRISMA 2020 Framework and general flattening techniques
3. export clean .csv for containing PRISMA reporting data, for use in PRISMA flowchart diagram (online at: https://estech.shinyapps.io/prisma_flowdiagram/)
4. extract keywords and cluster them into thematic groups
5. created a bar chart for the most frequent key words of out of all the groups
6. use keyword frequencies and link them with co-occurrence traces on a VOS Map (adjustable between frequency and co-occurrence node filtering)
7. Generate co-authorship vos map (through the topic modelling script)

---

## **Before running**


- make sure you have exported and inserted the most resent .ris export from mendeley into the "raw" data

> #### DO NOT CHANGE THE FILE JUST CHANGE THE CONTENTS!