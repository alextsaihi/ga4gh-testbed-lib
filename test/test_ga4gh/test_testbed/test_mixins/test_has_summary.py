import pytest
from ga4gh.testbed.report.case import Case
from ga4gh.testbed.report.test import Test
from ga4gh.testbed.report.phase import Phase
from ga4gh.testbed.report.report import Report

# setup 20 cases with specific statuses
case_statuses = [
    "UNKN", # 0
    "UNKN", # 1
    "SKIP", # 2
    "WARN", # 3
    "PASS", # 4
    "PASS", # 5
    "WARN", # 6
    "FAIL", # 7
    "FAIL", # 8
    "SKIP", # 9
    "UNKN", # 10
    "PASS", # 11
    "WARN", # 12
    "FAIL", # 13
    "FAIL", # 14
    "SKIP", # 15
    "SKIP", # 16
    "UNKN", # 17
    "WARN", # 18
    "PASS" # 19
]

def set_case_status(case_object, case_index):
    status_setters = {
        "UNKN": "set_status_unknown",
        "PASS": "set_status_pass",
        "WARN": "set_status_warn",
        "FAIL": "set_status_fail",
        "SKIP": "set_status_skip"
    }
    setter_fn_name = status_setters[case_statuses[case_index]]
    setter_fn = getattr(case_object, setter_fn_name)
    setter_fn()

def set_case_statuses_of_test(test, case_indices):
    for case_index in case_indices:
        case_object = test.add_case()
        set_case_status(case_object, case_index)

test_object_inputs = "case_indices,exp"
test_object_cases = [
    (
        [0, 1, 2, 3, 4],
        [2, 1, 1, 0, 1]
    ),
    (
        [5, 6, 7, 8, 9],
        [0, 1, 1, 2, 1]
    ),
    (
        [10, 11, 12, 13, 14],
        [1, 1, 1, 2, 0]
    ),
    (
        [15, 16, 17, 18, 19],
        [1, 1, 1, 0, 2]
    )
]

phase_object_inputs = "test_indices,exp"
phase_object_cases = [
    (
        [
            [0, 1, 2, 3, 4],
            [10, 11, 12, 13, 14]
        ],
        [3, 2, 2, 2, 1]
    )
]

@pytest.mark.parametrize(test_object_inputs, test_object_cases)
def test_summarize_test_object(case_indices, exp):
    test = Test()
    set_case_statuses_of_test(test, case_indices)
    test.summarize()

    summary = test.get_summary()
    unknown, passed, warn, fail, skip = exp
    
    assert summary.get_unknown() == unknown
    assert summary.get_passed() == passed
    assert summary.get_warned() == warn
    assert summary.get_failed() == fail
    assert summary.get_skipped() == skip

@pytest.mark.parametrize(phase_object_inputs, phase_object_cases)
def test_summarize_phase_object(test_indices, exp):
    phase = Phase()
    for case_indices in test_indices:
        test = phase.add_test()
        set_case_statuses_of_test(test, case_indices)
    
    phase.summarize()
    summary = phase.get_summary()
    unknown, passed, warn, fail, skip = exp

    assert summary.get_unknown() == unknown
    assert summary.get_passed() == passed
    assert summary.get_warned() == warn
    assert summary.get_failed() == fail
    assert summary.get_skipped() == skip

# def test_summarize_report_object():
#     pass
