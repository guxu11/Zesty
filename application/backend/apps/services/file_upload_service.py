import os
from apps.utils.utils import gen_random_string
from github import Github, Auth
from apps.constants.constants import REPO_NAME, BRANCH_NAME, GITHUB_USER_NAME
from apps.enums.response_status import ResponseStatus



class FileUploadService:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.auth = Auth.Token(self.token)

    def upload_img(self, file):
        response = {}
        try:
            if file:
                # convert file to bytearray
                filearray = bytes(file.read())
                deduplicated_filename = gen_random_string(5) + file.filename

                github = Github(auth=self.auth)
                repo = github.get_user().get_repo(REPO_NAME)

                commit_message = f'Upload image {file.filename}'
                repo.create_file(deduplicated_filename, commit_message, filearray, branch=BRANCH_NAME)
                
                # Construct the file URL
                file_url = f'https://raw.githubusercontent.com/{GITHUB_USER_NAME}/{REPO_NAME}/{BRANCH_NAME}/{deduplicated_filename}'
                response.update(UploadResponseStatus.SUCCESS)
                response.update({"data": {"url": file_url}})
        except Exception as e:
            response.update(UploadResponseStatus.FAIL)
        return response
        

class UploadResponseStatus(ResponseStatus):
    pass