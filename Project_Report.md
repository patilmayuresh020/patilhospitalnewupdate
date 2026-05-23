# Smart Hospital Management System - Project Report

## INDEX

| Sr. No. | Particulars |
| :---: | :--- |
| 1 | Abstract |
| 2 | Introduction |
| 3 | Proposed System |
| 4 | Need of the System |
| 5 | Software & Hardware Requirements |
| 6 | Database Diagrams (DFD / ERD / Use Case Diagrams) |
| 7 | Database Design |
| 8 | Project Screen Shots |
| 9 | Future Scope |
| 10 | Conclusion |
| 11 | References |

---

## 1. Abstract
The Smart Hospital Management System is a web-based comprehensive healthcare solution designed to streamline the hospital's daily operations. With digital interfaces for patients, doctors, and administrators, the system eliminates traditional paper-based processes. Patients can book appointments online, view real-time queue statuses, and access their medical history. Doctors can manage their schedules and issue digital medical reports, while administrators get a holistic overview of hospital operations through graphical statistics. The application utilizes a Python Flask backend integrated with a MySQL database to ensure data integrity, scalability, and seamless user experiences.

## 2. Introduction
The advent of digital technology has transformed numerous sectors, and healthcare is no exception. The traditional hospital management process is often characterized by long queues, mismanaged patient records, and inefficient doctor-patient communication. To address these challenges, the "Smart Hospital App" was conceptualized. This system provides a unified platform where users can seamlessly access hospital services, doctors can efficiently manage consultations, and administrators can monitor hospital performance. The project focuses on creating an intuitive user interface powered by a robust backend, ensuring quick and secure access to critical medical data.

## 3. Proposed System
The proposed Smart Hospital App is designed with a multi-portal architecture, specifically catering to three types of users:
- **Patient Portal**: Allows new and existing patients to log in using their mobile numbers, book appointments for various departments (General Physician, Dental, ENT, Orthopedic, Cardiology, Pediatrics), check doctor availability, monitor live queue times, and manage user profiles.
- **Doctor Portal**: Enables doctors to log in, view their scheduled appointments, update their availability status, and generate detailed digital medical reports containing diagnoses, prescribed medicines, symptoms, and follow-up dates.
- **Admin Portal**: A centralized dashboard for hospital administration to oversee total patients, doctors, and appointments, manage user accounts (adding new doctors or removing patients), and track the hospital's revenue and performance metrics.

## 4. Need of the System
- **Reduction of Wait Times**: By providing a live queue tracking feature, patients can plan their visits efficiently, reducing congestion in waiting rooms.
- **Centralized Data Management**: A digital database eliminates the risk of losing physical files, making patient history retrieval instantaneous for both patients and doctors.
- **Operational Efficiency**: Automated appointment bookings and streamlined doctor schedules reduce the manual workload of hospital staff.
- **Better Communication**: Features like health insights, blogs, and direct contact forms enhance hospital-patient engagement.
- **Data-Driven Administration**: The admin dashboard provides crucial statistics, aiding hospital management in better resource allocation and decision-making.

## 5. Software & Hardware Requirements

**Software Requirements:**
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla JS), SweetAlert2
- **Backend**: Python 3.x, Flask Framework
- **Database**: MySQL (XAMPP Server)
- **Environment**: Visual Studio Code, XAMPP Control Panel

**Hardware Requirements:**
- **Processor**: Intel Core i3 / AMD Ryzen 3 or higher
- **RAM**: 4 GB minimum (8 GB recommended)
- **Storage**: Minimum 500 MB free space for the application and database
- **Operating System**: Windows 10/11, macOS, or Linux

## 6. Database Diagrams (DFD / ERD / Use Case Diagrams)
*(Note: Please insert the actual graphical diagrams in your final printed report. The textual representation is provided below.)*

**Use Case Diagram Outline:**
- **Patient**: Books Appointment, Views Queue, Views Medical History, Reads Blogs.
- **Doctor**: Views Appointments, Updates Queue Status, Creates Medical Reports.
- **Admin**: Manages Doctors, Manages Patients, Views Dashboard Stats.

**ERD Outline:**
- `Users` Entity (id, name, mobile, role) has a one-to-many relationship with `Appointments`.
- `Appointments` Entity (id, dept, doctor_name, date) has a one-to-one relationship with `Reports`.
- `Reports` Entity (id, diagnosis, medicines, symptoms, follow_up_date) belongs to `Appointments`.

## 7. Database Design
The MySQL database `hospital_db` is normalized and structured to ensure data consistency. Key tables include:

1. **`users` Table**: Stores all types of users (patients, doctors, and admins).
   - columns: `id`, `name`, `age`, `mobile`, `role`, `department`, `education`, `status`, `queue_current`, `queue_total`, `room_number`, `description`, `created_at`
2. **`appointments` Table**: Manages all booking records.
   - columns: `id`, `dept`, `doctor_name`, `date`, `status`, `user_mobile`, `patient_name`, `patient_age`, `report_id`
3. **`reports` Table**: Stores medical records generated by doctors.
   - columns: `id`, `appointment_id`, `diagnosis`, `medicines`, `notes`, `file_path`, `symptoms`, `follow_up_date`, `created_at`
4. **`messages` Table**: Stores inquiries from the contact form.
   - columns: `id`, `name`, `subject`, `message`, `created_at`

## 8. Project Screen Shots
*(Note: Please insert the screenshots of your application here before printing your final report.)*
1. **Home/Login Screen**: Patient login via mobile number.
2. **Patient Dashboard**: Appointment booking, live queue, health insights, and contact form.
3. **Doctor Portal**: List of patient appointments and status toggles.
4. **Medical Report Form**: Doctor interface for adding diagnosis and medicines.
5. **Admin Dashboard**: Overview of hospital statistics, revenue, and active users.
6. **Admin Doctor Management**: Interface to add or remove doctor profiles.

## 9. Future Scope
- **Online Payment Integration**: Allowing patients to pay consultation fees directly through the app using services like Razorpay or Stripe.
- **Telemedicine & Video Consultations**: Integrating real-time video calls for remote patient-doctor interactions.
- **AI-Powered Chatbots**: Providing automated symptom checking and 24/7 patient support.
- **Notifications**: Implementing SMS and Email APIs to alert patients regarding their upcoming appointments and turn in the queue.
- **Mobile Application**: Developing native Android and iOS mobile applications for more accessible smartphone usage.

## 10. Conclusion
The Smart Hospital Management System successfully achieves its goal of digitizing hospital workflows. By bridging the gap between healthcare providers and patients through a responsive web interface, the system brings transparency, speed, and reliability to the medical appointment process. With dedicated modules for all stakeholders and a scalable MySQL database, the application serves as a robust foundation for modern digital healthcare facilities and is well-equipped to handle future feature expansions.

## 11. References
1. Flask Documentation: https://flask.palletsprojects.com/
2. MySQL Reference Manual: https://dev.mysql.com/doc/
3. JavaScript MDN Web Docs: https://developer.mozilla.org/en-US/docs/Web/JavaScript
4. SweetAlert2 Library: https://sweetalert2.github.io/
5. HTML & CSS Tutorials: https://www.w3schools.com/

तुमच्या प्रोजेक्ट रिपोर्टसाठी 

start_hospital.bat
 या फाईलची माहिती आणि तिची काम करण्याची प्रक्रिया (Process) खालीलप्रमाणे मराठीत दिली आहे. तुम्ही ही माहिती तुमच्या रिपोर्टमध्ये किंवा सादरीकरणाच्या (Presentation) वेळी वापरू शकता:


start_hospital.bat
 म्हणजे काय?

start_hospital.bat
 ही एक विंडोज बॅच फाईल (Windows Batch File) आहे. तिचा मुख्य उद्देश तुमचा 'स्मार्ट हॉस्पिटल' (Smart Hospital) प्रोजेक्ट आणि त्याचा सर्वर फक्त एका क्लिकवर (One-click) चालू करणे हा आहे. यामुळे प्रत्येक वेळी मॅन्युअली कमांड्स टाईप करण्याची गरज पडत नाही.

ही फाईल नक्की कशी काम करते (Process of Execution):
१. सुरुवात आणि पूर्वसूचना (Initialization & Background Check): जेव्हा तुम्ही या फाईलवर डबल-क्लिक करून ती उघडता, तेव्हा एक काळी स्क्रीन (Command Prompt) उघडते आणि स्क्रीनचा रंग हिरवा (Color 0A) होतो. सर्वात आधी ती तुम्हाला तुमचा MySQL Server (जसे की XAMPP मधील MySQL) सुरू असल्याची खात्री करायला सांगते. कारण डेटाबेस सुरू नसेल तर ॲप्लिकेशन व्यवस्थित काम करू शकणार नाही.

२. पायथन बॅकएंड सर्वर सुरू करणे (Starting Flask Backend): दोन सेकंद थांबल्यानंतर, ही सिस्टीम आपोआप तुमच्या प्रोजेक्टमधील backend नावाच्या फोल्डरमध्ये जाते. तिथे गेल्यावर ती एक नवीन दुसरी कमांड विंडो उघडते आणि python server.py ही कमांड चालवते. या कमांडमुळे तुमचा पायथनचा फ्लास्क (Python Flask) सर्वर सुरू होतो आणि डेटाबेससोबत कनेक्ट होतो.

३. आपोआप ब्राउझर उघडणे (Auto-Launching the Website): बॅकएंड सर्वर पूर्णपणे सुरू होण्यासाठी ही फाईल स्वतःच ३ सेकंद थांबते (Timeout). त्यानंतर, ती आपोआप तुमचा डिफॉल्ट वेब ब्राउझर (उदा. Google Chrome किंवा Edge) चालू करते आणि त्यात http://127.0.0.1:5000 (Localhost) ही वेबसाइटची लिंक ओपन करते. यामुळे तुम्हाला मॅन्युअली लिंक टाईप करावी लागत नाही.

४. शेवटी माहिती दर्शवणे (Final System Checks): सगळं व्यवस्थित चालू झाल्यावर, त्या काळ्या स्क्रीनवर तुम्हाला तुमची वेबसाइट लिंक आणि डेटाबेस मॅनेज करण्यासाठीची माहिती दिसते. ही कमांड विंडो लगेच बंद होऊ नये म्हणून शेवटी ती थांबते आणि 'Press any key to close this window...' असा मेसेज देते.

थोडक्यात सांगायचे तर (Summary):
ही 

.bat
 फाईल तुमच्या प्रोजेक्टचे ऑटोमेशन (Automation) करते. ती स्वतःहून सर्वर चालू करते, बॅकएंड रन करते आणि युजरसाठी सोप्या पद्धतीने ब्राउझरमध्ये वेबसाइट उघडून देते. हे एका चांगल्या सॉफ्टवेअर सिस्टीमचे उत्तम उदाहरण आहे!

