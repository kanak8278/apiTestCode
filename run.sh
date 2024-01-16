#!/bin/bash

run_login() {
    python main.py login --headers '{"Content-Type": "application/json", "Custom-Header": "Value"}' --body '{"username": "USERNAME", "password": "PASSWORD", "fcm_id": "NA", "role": "applicant"}'
}

run_profile_details() {
    python main.py profile_details --headers '{"Content-Type": "application/json", "Authorization": "Bearer YOUR_TOKEN", "X-User-Guid": "YOUR_USER_GUID", "X-User-Role": "applicant", "Language": "en"}' --body '{}'
}

run_get_advocate_list() {
    python main.py get_advocate_list --headers '{"Content-Type": "application/json", "Language": "en", "Authorization": "Bearer YOUR_TOKEN", "X-User-Guid": "YOUR_USER_GUID", "X-User-Role": "applicant"}' --body '{"state_code": "9135", "slot_date": "2024-01-16", "district_code": "913502", "gender": "Male", "language": "8", "category_id": "144"}'
}

run_get_slot() {
    python main.py get_slot --headers '{"Content-Type": "application/json", "Language": "en", "Authorization": "Bearer YOUR_TOKEN", "X-User-Guid": "YOUR_USER_GUID", "X-User-Role": "applicant"}' --body '{"advocate_id": "257", "date": "2024-01-18"}'
}

run_case_otp_send() {
    python main.py case_otp_send --headers '{"Content-Type": "application/json", "Authorization": "Bearer YOUR_TOKEN", "X-User-Guid": "YOUR_USER_GUID", "X-User-Role": "applicant", "Language": "en"}' --body '{"mobile": "NUMBER"}'
}

run_case_otp_validate() {
    python main.py case_otp_validate --headers '{"Content-Type": "application/json", "Next-Request-Token": "YOUR_NEXT_REQUEST_TOKEN", "Authorization": "Bearer YOUR_TOKEN", "X-User-Guid": "YOUR_USER_GUID", "X-User-Role": "applicant", "Language": "en"}' --body '{"mobile": "NUMBER", "otp": "YOUR_OTP"}'
}

run_add_case() {
    python main.py add_case --headers '{"Content-Type": "application/json", "Language": "en", "Authorization": "Bearer YOUR_TOKEN", "X-User-Guid": "YOUR_USER_GUID", "Next-Request-Token": "YOUR_NEXT_REQUEST_TOKEN", "X-User-Role": "applicant"}' --body '{"advocate_id": "226", "case_documents": [], "case_type_id": "129", "date": "2024-01-17", "case_sub_type_id": "160", "slot_id": "22", "summary": "Testing Complaint"}'
}

run_master_api() {
    python main.py master_api --headers '{"Content-Type": "application/json", "Language": "en"}' --body '{"type": 8}'
}

case "$1" in
    login)
        run_login
        ;;
    profile_details)
        run_profile_details
        ;;
    get_advocate_list)
        run_get_advocate_list
        ;;
    get_slot)
        run_get_slot
        ;;
    case_otp_send)
        run_case_otp_send
        ;;
    case_otp_validate)
        run_case_otp_validate
        ;;
    add_case)
        run_add_case
        ;;
    master_api)
        run_master_api
        ;;
    *)
        echo "Invalid API name. Please provide a valid API name."
        exit 1
        ;;
esac

