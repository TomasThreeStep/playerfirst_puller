import requests
import json
from typing import Dict, Optional


class PlayerFirstAPI:
    def __init__(self):
        self.base_url = "https://playerfirst-staging.azurewebsites.net/api"
        self.auth_url = f"{self.base_url}/auth"
        self.roster_url = f"{self.base_url}/roster/division/135802"
        self.jwt_token = None
        self.user_id = None

    def authenticate(self, username: str, password: str):

        response = requests.post(
            self.auth_url,
            json={
                "username": username,
                "password": password
            },
            headers={"Content-Type": "application/json"}
        )

        auth_response = response.json()

        self.jwt_token = auth_response.get('jwt')
        self.user_id = auth_response.get('userId')



    def get_roster_data(self) -> Optional[Dict]:

        if not self.jwt_token:
            return None

        response = requests.get(self.roster_url, headers={
            "Authorization": f"Bearer {self.jwt_token}",
            "Content-Type": "application/json"
        })

        return response.json()



def main():
    api_client = PlayerFirstAPI()

    username = "ron.sandstrom@threestep.com"
    password = "Apple12!"


    api_client.authenticate(username, password)
    roster_data = api_client.get_roster_data()
    roster_data = roster_data["roster"]
    if roster_data:
        print("\n" + "=" * 50)
        print("ROSTER DATA:")
        print("=" * 50)
        print(json.dumps(roster_data, indent=4))

    else:
        print("Authentication failed. Cannot proceed.")


if __name__ == "__main__":
    main()