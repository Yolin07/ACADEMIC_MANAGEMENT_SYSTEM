DATA_PRIVACY_TERMS = """
╔══════════════════════════════════════════════════════════════════╗
║          DATA PRIVACY POLICY & TERMS OF USE                     ║
║          Secure Grade Management System                         ║
║          In Compliance with Republic Act No. 10173              ║
║          (Data Privacy Act of 2012, Philippines)                ║
╚══════════════════════════════════════════════════════════════════╝

Effective Date: January 1, 2025
Last Updated: May 2025

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. PURPOSE AND SCOPE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This Secure Grade Management System ("the System") is designed
to help authorized educators manage academic records of students.
This Privacy Policy explains how personal data is collected,
used, stored, and protected within the System.

This policy applies to:
  • Registered teachers and administrators using the System
  • Student academic records entered into the System
  • All data stored in the local SQLite database

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. DATA COLLECTED
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

The System collects and processes the following personal data:

  FOR EDUCATORS / ADMINISTRATORS:
  ▸ Username (used as unique identifier)
  ▸ Password (stored using PBKDF2-SHA256 hashing with salt —
    your actual password is NEVER stored in plain text)
  ▸ Security recovery question and answer (hashed)

  FOR STUDENTS (entered by authorized educators):
  ▸ Student ID / Matrix Number
  ▸ Full Name
  ▸ Subject names and corresponding numeric grades
  ▸ Academic period classifications (Prelim, Midterm, Final,
    or quarterly equivalents)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. PURPOSE OF DATA PROCESSING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Personal data is collected and processed solely for the
following legitimate educational purposes:

  ✔ Authenticating authorized system users
  ✔ Organizing and maintaining student grade records
  ✔ Computing General Weighted Average (GWA) and academic
    standing (PASSED / REMEDIAL / INCOMPLETE)
  ✔ Facilitating secure account recovery
  ✔ Supporting academic reporting and record management

Data will NOT be used for:
  ✘ Commercial profiling or targeted advertising
  ✘ Selling or sharing data with third parties
  ✘ Any purpose unrelated to academic record management

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. DATA STORAGE AND SECURITY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ▸ All data is stored LOCALLY on the device in a SQLite
    database file ("secured_academic.db").
  ▸ The System does NOT transmit data to any external server,
    cloud service, or third-party platform.
  ▸ Passwords and security answers are protected using
    PBKDF2-HMAC-SHA256 with a unique salt per entry and
    100,000 hash iterations, in accordance with industry
    security standards.
  ▸ Physical and logical access to the database file should be
    restricted to authorized personnel only.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. DATA RETENTION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  ▸ Data is retained for as long as the System is actively
    used or until manually deleted by authorized users.
  ▸ Educators may purge student records or entire class
    directories at any time through the System interface.
  ▸ Account deletion removes all associated records through
    cascading database constraints.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. RIGHTS OF DATA SUBJECTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

In accordance with RA 10173 (Data Privacy Act of 2012),
data subjects have the following rights:

  ▸ Right to be Informed — to know how their data is collected
    and used (this Policy)
  ▸ Right to Access — to request access to their personal data
  ▸ Right to Correction — to request correction of inaccurate
    data
  ▸ Right to Erasure — to request deletion of their data
  ▸ Right to Object — to object to processing of their data
  ▸ Right to Data Portability — to receive a copy of their
    data in a portable format

To exercise these rights, contact the system administrator
or the teacher managing the records.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. RESPONSIBILITIES OF REGISTERED USERS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

By registering and using this System, you agree to:

  ✔ Enter only accurate and truthful academic data
  ✔ Keep your login credentials confidential
  ✔ Use the System exclusively for legitimate educational
    record-keeping purposes
  ✔ Report any unauthorized access or data breach immediately
  ✔ Comply with RA 10173 and other applicable laws when
    handling student personal data
  ✔ Ensure students or their guardians are informed that their
    academic data is being recorded digitally

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. CONSENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

By checking the "I have read and agree to the Data Privacy
Terms" checkbox during registration, you:

  ✔ Acknowledge that you have read and understood this policy
  ✔ Consent to the collection and processing of your account
    data as described herein
  ✔ Accept responsibility for the student data you enter into
    the System
  ✔ Agree to use the System in compliance with applicable
    data protection laws

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. CHANGES TO THIS POLICY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This policy may be updated to reflect changes in the System
or applicable law. Continued use of the System after changes
constitutes acceptance of the revised policy.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. CONTACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For any data privacy concerns or requests, please contact the
designated Data Privacy Officer (DPO) of your institution or
the administrator of this System.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    By proceeding, you confirm your full agreement to these terms.
    This System is committed to protecting your data and the
    privacy of all students in your care.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

