# Milestone: Jupyter Notebook Navigation & Environment Verification

## Overview

This milestone focuses on learning how to correctly launch and operate Jupyter Notebook within a local Data Science environment.

The goal is not to perform analysis, but to build confidence in:

- Launching Jupyter properly  
- Understanding the interface  
- Navigating folders intentionally  
- Creating notebooks in the correct location  
- Managing notebook files safely  

This milestone ensures that the development environment is organized and fully functional before beginning notebook-based Data Science work.

---

## Why This Milestone Matters

Many early Data Science workflow issues occur because of:

- Running Jupyter from the wrong directory  
- Creating notebooks in unintended locations  
- Losing track of datasets or notebooks  
- Using the wrong Conda environment or kernel  
- Poor file organization  

This milestone ensures:

- Notebooks live in the correct project folder  
- The correct Python environment is active  
- Files are structured intentionally  
- Workflow mistakes are avoided early  

Think of this as understanding your workspace before beginning technical work.

---

## What Was Required

This milestone required the following:

1. Launch Jupyter Notebook from the terminal  
2. Explore and understand the Jupyter Home interface  
3. Navigate project folders intentionally  
4. Create and open a notebook  
5. Verify the notebook runs correctly  
6. Practice basic notebook file management  
7. Record a short walkthrough video (~2 minutes)  

No data analysis or modeling was performed.

---

## Steps Performed

### 1. Activated the Correct Conda Environment

Activated the appropriate Conda environment before launching Jupyter to ensure correct kernel usage and package isolation.

```bash
conda activate <environment-name>
```

This ensures the notebook uses the correct Python interpreter and installed packages.

---

### 2. Launched Jupyter Notebook from Terminal

Navigated to the intended project directory:

```bash
cd <project-folder>
```

Launched Jupyter:

```bash
jupyter notebook
```

Verified that:

- Jupyter opened successfully in the web browser  
- The root directory displayed matches the folder from which it was launched  

This confirms awareness of the working directory.

---

### 3. Explored the Jupyter Home Interface

Identified and understood:

- File and folder listing area  
- Navigation breadcrumbs  
- "New" button for creating notebooks  
- File type indicators (`.ipynb`, `.py`, folders)  

Confirmed that the interface directly maps to the local file system.

---

### 4. Navigated Project Directories

Practiced:

- Entering folders  
- Returning to parent directories using breadcrumbs  
- Locating the correct project folder  

Confirmed understanding of where files are being saved at all times.

---

### 5. Created and Verified a Notebook

Created a new notebook inside the correct project folder:

**New → Python 3**

Renamed the notebook appropriately.

Executed a test cell:

```python
print("Jupyter is working!")
```

Verified that:

- The cell executed successfully  
- The Python kernel was active  
- The expected Conda environment was being used  

This confirms the notebook environment is functioning correctly.

---

### 6. Practiced Notebook File Management

Performed the following actions:

- Renamed the notebook  
- Saved changes  
- Closed the notebook safely  
- Reopened it from the Home interface  

Confirmed that notebooks can be managed without confusion or accidental file loss.

---