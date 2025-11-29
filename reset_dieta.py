from dotenv import load_dotenv
import os
from notion_client import Client

load_dotenv()

notion = Client(auth=os.getenv("TOKEN"))

PAGE_ID = os.getenv("PAGE_ID")

children = notion.blocks.children.list(PAGE_ID)['results']

for block in children:
    if block["type"] == "heading_1":
        texto = block["heading_1"]["rich_text"][0]["plain_text"].strip().lower()
    if texto == "refeições" and block["type"] == "to_do" and block["to_do"]["checked"] == True:
        notion.blocks.update(
            block_id=block["id"],
            to_do={"checked": False}
        )
        print(
            f"Refeição '{block['to_do']['rich_text'][0]['plain_text']}' resetada para não concluída.")
    
    if texto == "refeições" and block["type"] == "to_do" and block['has_children'] == True:
        notion_children = notion.blocks.children.list(
            block['id'])['results']
        for child in notion_children:
            if child["type"] == "to_do" and child["to_do"]["checked"] == True:
                notion.blocks.update(
                    block_id=child["id"],
                    to_do={"checked": False}
                )
                print(
                    f"Refeição '{child['to_do']['rich_text'][0]['plain_text']}' resetada para não concluída.")
