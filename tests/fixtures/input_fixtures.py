import pytest

@pytest.fixture
def new_data_from_paste():
    return """2045-07-10
- 8h Vacation INT-73
2045-07-11
- 8h National Holiday INT-63
2045-07-12
- 1h Product Questions with HoA IPJ-64
- 1h TMM Team daily TMM-256
- 1.5h TMM Sprint Planning TMM-128
- 0.5h Working on production bug TMM-512
- 0.5h Working on production bug TMM-513
- 1.5h Working on production bug TMM-514
- 1h Backlog Refinement TMM-32
- 0.5h Code Reviews TMM-16
- 0.5h Working on production bug TMM-513
2045-07-13
- 0.5h Working on Story TMM-625
- 0.5h Working on Story TMM-626
- 0.5h TMM Team daily TMM-256
- 1h Working on Story TMM-626
- 4h Working on Story TMM-625
- 1h Code Reviews TMM-16
- 0.5h Product Questions with HoA IPJ-64
2045-07-14
- 8h National Holiday INT-75
"""

@pytest.fixture
def already_logged_data_from_paste():
    return """2045-07-03
- 2h Do some important stuff! IPJ-170
- 6h Requirements Workshop! ISTN-87
2045-07-04
- 8h Vacation INT-762
2045-07-05
- 0.5h Daily Scrum IPJ-101
- 1.5h Code reviews IPJ-117
- 4h Requirements Workshop! ISTN-87
- 2h Shuttle testing ISTN-221
2045-07-06
- 8h Vacation INT-762
2045-07-07
- 0.5h Daily Scrum IPJ-101
- 2h Backlog Refinement IPJ-207
- 2.5h Sprint Planning IPJ-271
- 3h Shuttle testing ISTN-221
"""

@pytest.fixture
def already_logged_data_from_file():
    return """=====================================================================
2045-06-19
- 8h Vacation INT-73
2045-06-20
- 8h National Holiday INT-63
2045-06-21
- 1h Product Questions with HoA IPJ-64
- 1h TMM Team daily TMM-256
- 1.5h TMM Sprint Planning TMM-128
- 0.5h Working on production bug TMM-512
- 0.5h Working on production bug TMM-513
- 1.5h Working on production bug TMM-514
- 1h Backlog Refinement TMM-32
- 0.5h Code Reviews TMM-16
- 0.5h Working on production bug TMM-513
2045-06-22
- 0.5h Working on Story TMM-625
- 0.5h Working on Story TMM-626
- 0.5h TMM Team daily TMM-256
- 1h Working on Story TMM-626
- 4h Working on Story TMM-625
- 1h Code Reviews TMM-16
- 0.5h Product Questions with HoA IPJ-64
2045-06-23
- 8h National Holiday INT-75
=====================================================================
2045-06-26
- 1.5h JIRA Management - TMM-19
- 3.5h Requirements Workshop IPJ-925
- 1h Working on production bug IPJ-523
- 1h Working on production bug IPJ-527
- 1h Working on production bug IPJ-541
2045-06-27
- 0.5h IPJ Team daily IPJ-52
- 2.5h IPJ Sprint Retrospective IPJ-52
- 2h Code Reviews IPJ-512
- 3h Working on Story IPJ-971
2045-06-28
- 4h Drag & drop POC IPJ-930
- 0.5h IPJ Team daily IPJ-52
- 2h Code Reviews IPJ-512
- 1.5h Working on Story IPJ-971
2045-06-29
- 1h IPJ Team daily IPJ-52
- 0.5h Sync with architecture IPJ-100
- 1.5h Assist with DB troubleshooting IPJ-977
- 0.5h Product Questions with HoA IPJ-64
- 1h Team Staffing Discussion IPJ-8
- 1h Drag & drop POC IPJ-930
- 1h Working on Story IPJ-971
- 0.5h Working on production bug IPJ-941
- 0.5h Working on production bug IPJ-942
- 0.5h Code Reviews IPJ-512
2045-06-30
- 8h Vacation INT-73
=====================================================================
2045-07-03
- 2h Do some important stuff! IPJ-170
- 6h Requirements Workshop! ISTN-87
2045-07-04
- 8h Vacation INT-762
2045-07-05
- 0.5h Daily Scrum IPJ-101
- 1.5h Code reviews IPJ-117
- 4h Requirements Workshop! ISTN-87
- 2h Shuttle testing ISTN-221
2045-07-06
- 8h Vacation INT-762
2045-07-07
- 0.5h Daily Scrum IPJ-101
- 2h Backlog Refinement IPJ-207
- 2.5h Sprint Planning IPJ-271
- 3h Shuttle testing ISTN-221
=====================================================================
=====================================================================
================Product Clarification Meetings TMM-64================
================TMM Code Validation TMM-16===========================
================TMM Scrum Ceremonies TMM-32==========================
================IPJ Scrum Ceremonies IPJ-52==========================
================IPJ Code Validation IPJ-512==========================
================General Company Meeting CMP-10=======================
================JIRA Management - TMM-19=============================
=====================================================================
"""

@pytest.fixture
def new_data_from_file():
    return """=====================================================================
2045-06-26
- 1.5h JIRA Management - TMM-19
- 3.5h Requirements Workshop IPJ-925
- 1h Working on production bug IPJ-523
- 1h Working on production bug IPJ-527
- 1h Working on production bug IPJ-541
2045-06-27
- 0.5h IPJ Team daily IPJ-52
- 2.5h IPJ Sprint Retrospective IPJ-52
- 2h Code Reviews IPJ-512
- 3h Working on Story IPJ-971
2045-06-28
- 4h Drag & drop POC IPJ-930
- 0.5h IPJ Team daily IPJ-52
- 2h Code Reviews IPJ-512
- 1.5h Working on Story IPJ-971
2045-06-29
- 1h IPJ Team daily IPJ-52
- 0.5h Sync with architecture IPJ-100
- 1.5h Assist with DB troubleshooting IPJ-977
- 0.5h Product Questions with HoA IPJ-64
- 1h Team Staffing Discussion IPJ-8
- 1h Drag & drop POC IPJ-930
- 1h Working on Story IPJ-971
- 0.5h Working on production bug IPJ-941
- 0.5h Working on production bug IPJ-942
- 0.5h Code Reviews IPJ-512
2045-06-30
- 8h Vacation INT-73
=====================================================================
2045-07-03
- 2h Do some important stuff! IPJ-170
- 6h Requirements Workshop! ISTN-87
2045-07-04
- 8h Vacation INT-762
2045-07-05
- 0.5h Daily Scrum IPJ-101
- 1.5h Code reviews IPJ-117
- 4h Requirements Workshop! ISTN-87
- 2h Shuttle testing ISTN-221
2045-07-06
- 8h Vacation INT-762
2045-07-07
- 0.5h Daily Scrum IPJ-101
- 2h Backlog Refinement IPJ-207
- 2.5h Sprint Planning IPJ-271
- 3h Shuttle testing ISTN-221
=====================================================================
2045-07-10
- 8h Vacation INT-73
2045-07-11
- 8h National Holiday INT-63
2045-07-12
- 1h Product Questions with HoA IPJ-64
- 1h TMM Team daily TMM-256
- 1.5h TMM Sprint Planning TMM-128
- 0.5h Working on production bug TMM-512
- 0.5h Working on production bug TMM-513
- 1.5h Working on production bug TMM-514
- 1h Backlog Refinement TMM-32
- 0.5h Code Reviews TMM-16
- 0.5h Working on production bug TMM-513
2045-07-13
- 0.5h Working on Story TMM-625
- 0.5h Working on Story TMM-626
- 0.5h TMM Team daily TMM-256
- 1h Working on Story TMM-626
- 4h Working on Story TMM-625
- 1h Code Reviews TMM-16
- 0.5h Product Questions with HoA IPJ-64
2045-07-14
- 8h National Holiday INT-75
=====================================================================
=====================================================================
================Product Clarification Meetings TMM-64================
================TMM Code Validation TMM-16===========================
================TMM Scrum Ceremonies TMM-32==========================
================IPJ Scrum Ceremonies IPJ-52==========================
================IPJ Code Validation IPJ-512==========================
================General Company Meeting CMP-10=======================
================JIRA Management - TMM-19=============================
=====================================================================
"""