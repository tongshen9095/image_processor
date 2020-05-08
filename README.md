# Medical Image Database

The program builds a medical image database. With the GUI, user can
- Upload an image
- Display an image
- Download an image
- Process an image, i.e. invert an image
- Compare two images

The server is hosted on duke vm: `vcm-14274.vm.duke.edu`. [Here](https://drive.google.com/file/d/1h9aNJgtQ7ay0TcS8B0Wji6i-VyG1j_MW/view?usp=sharing) is a video demo for the program.

## APIs
The server provides six APIs.

- POST /api/new_img
 
  The API adds new images to database. `name` is the primary key.

  Sample input
  ```
  {
      "name": str,  # name of the image
      "b64str": str,  # base64 representation of the image
      "imgsize": str,  # image size, width x height
      "processed": bool, # whether the image is processed or not
      "timestamp": str  # timestamp when adding the image
  }
  ```

- GET /api/all_imgs
   
    The API gets a list of images names storing in the database. The list is sorted alphabetically.

    Sample output
    ```
    ["acl1.jpg","acl1_proecessed.jpg","esophagus 1.jpg"]
    ```

- GET `/api/all_imgs/<processed>`

    The API receives process status in URL, "0": unprocessed, "1": processed and returns a list of names of selected images. The list is sorted alphabetically.

    Sample output when `processed = "1"`
    ```
    ["acl1_proecessed.jpg","synpic51041_proecessed.jpg"]
    ```

- GET /api/process_img/<img_name>

    The API receives image name in URL and process the selected image.

- GET /api/img/<img_name>

    The API receives image name in URL and returns image information in an dictionary.

    Sample output
    ```
    {
        "name": str,  # name of the image
        "b64str": str,  # base64 representation of the image
        "imgsize": str,  # image size, width x height
        "processed": bool, # whether the image is processed or not
        "timestamp": str  # timestamp when adding the image
    }
    ```

- GET /api/del/<img_name>

    The API receives image name in URL and deletes the image in database.

## Run the program
- Clone the repository onto your local computer.
    ```
    git clone <HTTPS>
    ```

- Create a python virtual environment and activate the vm.

    ```
    python -m venv <VirtualEnvironmentName>
    source <VirtualEnvironmentName>/bin/activate
    ```
- Install the required packages listed in ```requirement.txt``` file
    
    ```
    pip install -r requirements.txt
    ```

- Open the client site
    ```
    python client.py
    ```

[![Build Status](https://travis-ci.com/BME547-Spring2020/final-project-tongshen9095.svg?token=ux78qpJUFtLc2BCMkjZA&branch=master)](https://travis-ci.com/BME547-Spring2020/final-project-tongshen9095)

Licensed under the [MIT License](LICENSE.txt)
