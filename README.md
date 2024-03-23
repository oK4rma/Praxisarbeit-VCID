# IFA VCID - Comapny Vehicles App

Subject content
• Datenbanken und Webentwicklung (DBWE)
• IT-Architektur (ITAR)
• Virtualisierung und Cloud Computing (VICC)

## Why this Project?

As part of this qualification-relevant practical work, what has been learned is intended to be used in a practical context application come.

### Exact work order

Your practical work should deliver the following results:
• An executable application with Flask and a database
• A short documentation on how to use the application
• A comprehensible description of the architecture of the software, especially if from the
  Technologies and procedures are deviated from teaching.
• A platform on which the application is deployed in the cloud
• Documentation of the selected platform(s), technology(s), architecture and solution approaches
  as well as reflecting on why this was chosen, what the benefits and potential risks are
  brings.
• Reflection on scalability, high availability, porting and possible challenges
  operational operations.

## Getting Started

### Prerequisites

You should have a virtual machine Ubuntu Linux.

### Installation

Please follow these steps so that everything works:

1. **Install git
  ```bash
   sudo apt install -y git
   ```

2. **Clone the Repository:**

   ```bash
   git clone https://github.com/oK4rma/Praxisarbeit_VCID_Steiner_Tobyas.git
   ```

2. **Navigate to the Directory:**

   ```bash
   cd Praxisarbeit_VCID_Steiner_Tobyas
   ```

4. **Start application**

   ```bash
   docker compose up --build
   ```
  This will now install all requiremtens from the "requirements.txt" and will start the application with NGINX and GUNICORN

5. **Running application**

   Since the application has been completely containerized, the Linux machine can simply be closed when it is hosted. The application continues to run in the background.

6. **Stop application**

    The application can be stpotted using the key combination “CTRL” + “C”.
 

## Testing

To do this, the file “boot.sh” must be started. This creates a test environment, installs all requirements and runs the three automated tests. If these have been carried out successfully, the manual tests can also be carried out.

```bash
./boot.sh
```
