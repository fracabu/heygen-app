[![HeyGen Hub](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/HeyGen-Primary-Logo-White-RGB-1-1--4a55668c-ba70-4da8-9e43-f26cf8dee2f0-1758033336009.png?fit=scale-down&width=120)\\
\\
![HeyGen Hub Logo](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/HeyGen-Primary-Logo-White-RGB-1-1-Small-9ccf5671-06d3-45e5-ba03-24938d8ea8dc-1758032578271.png?fit=scale-down&width=50)](https://community.heygen.com/)

HeyGen Hub

- [Home](https://community.heygen.com/)
- [Forum](https://community.heygen.com/public/forum)
- [Events](https://community.heygen.com/public/events)
- [Resources](https://community.heygen.com/public/content)
- [Groups](https://community.heygen.com/public/clubs)
- Chat

- Help

- More


Search

-05:00 EST

SIGN IN

- [Home](https://community.heygen.com/)
- [Forum](https://community.heygen.com/public/forum)
- [Events](https://community.heygen.com/public/events)
- [Resources](https://community.heygen.com/public/content)
- [Groups](https://community.heygen.com/public/clubs)
- Chat

- Help


[Groups](https://community.heygen.com/home/clubs)

/

[API Developers](https://community.heygen.com/public/clubs/api-builders-au0/overview)

/

[Content](https://community.heygen.com/public/clubs/api-builders-au0/content)

API & Integrations

December 12, 2024 · Last updated on May 20, 2025

# Send personalized messages using HeyGen’s API: a step-by-step walkthrough

![Send personalized messages using HeyGen’s API: a step-by-step walkthrough](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/46-9bd09889-4b20-40e7-8ecc-ab63e9858b0f-1733984377672.png?fit=scale-down&width=400)

\# API

\# Personalized Video

## Creating personalized birthday videos using templates and integrating OpenAI to generate dynamic scripts

[Share via email](mailto:?subject=%5BHeyGen%20Hub%5D%20Send%20personalized%20messages%20using%20HeyGen%E2%80%99s%20API%3A%20a%20step-by-step%20walkthrough&body=https%3A%2F%2Fcommunity.heygen.com%2Fpublic%2Fclubs%2Fapi-builders-au0%2Fresources%2Fhow-to-use-heygens-api-a-step-by-step-walkthrough)

![Send personalized messages using HeyGen’s API: a step-by-step walkthrough](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/46-9bd09889-4b20-40e7-8ecc-ab63e9858b0f-1733984377672.png?fit=scale-down&width=400)

HeyGen’s API empowers you to automate video creation, personalize content at scale, and integrate avatars into your projects. Want to see what a personalized video from HeyGen looks like? [Fill out this form](https://2ykg0d9nevz.typeform.com/demo-pv) to receive one.

In this guide, we’ll demonstrate two examples based on [Alec’s webinar](https://www.youtube.com/watch?v=yJGwWwPd-qA):

**1) Creating Personalized Birthday Videos Using Templates**

**2) Integrating OpenAI to Generate Dynamic Scripts**

HeyGen-API - YouTube

[Photo image of HeyGen](https://www.youtube.com/channel/UCV0FmNF3iM-022BF1KbVtxA?embeds_referring_euri=https%3A%2F%2Fcommunity.heygen.com%2F)

HeyGen

66.6K subscribers

[HeyGen-API](https://www.youtube.com/watch?v=yJGwWwPd-qA)

HeyGen

Search

Info

Shopping

Watch later

Share

Copy link

Tap to unmute

If playback doesn't begin shortly, try restarting your device.

You're signed out

Videos you watch may be added to the TV's watch history and influence TV recommendations. To avoid this, cancel and sign in to YouTube on your computer.

CancelConfirm

More videos

## More videos

Share

Include playlist

An error occurred while retrieving sharing information. Please try again later.

[Watch on](https://www.youtube.com/watch?t=1733984239317&v=yJGwWwPd-qA&embeds_referring_euri=https%3A%2F%2Fcommunity.heygen.com%2F)

20069262:00:41:57

20069262:00:41:57 / 40:05

•Live

•

﻿

﻿

Let’s get started!

## **Step 1: Access the HeyGen API Documentation**

Visit﻿ [**docs.heygen.com**](https://docs.heygen.com/) to access HeyGen’s official API documentation. This contains:

- Setup guides for beginners.

- Detailed API references for developers.

If you’re unfamiliar with APIs, don’t worry—this guide will walk you through the essentials.

## **Step 2: Create a Video Template**

Templates allow you to design reusable videos with customizable elements (variables). These templates are central to automating video creation.

### **How to Create a Template:**

1. **Log into HeyGen** and navigate to the **Templates** section.

2. Click **Create Template** and design your video:

- Add your **avatar**, **background**, and any static elements (e.g., text, images).

3. **Define Variables** for dynamic content:

- Select an element (e.g., text or image).

- Click the **API** button to assign a variable name (e.g., name, message, background).

4. Save the template and copy its **Template ID** by clicking the three dots next to the template.

## **Step 3: Generate Videos Using the Template API**

### **Python Example:**

Below is a corrected script to dynamically generate a personalized birthday video:

```
import requests
﻿

# API and Template Information
api_key = "YOUR_API_KEY"
template_id = "YOUR_TEMPLATE_ID"
generate_url = f"https://api.heygen.com/v2/template/{template_id}/generate"
﻿

# Request Headers
headers = {"Accept": "application/json", "X-API-KEY": api_key}
﻿

# Payload with Dynamic Variables
payload = {
    "title": "Birthday Greeting for Alec",
    "variables": {
        "name": {"name": "name", "type": "text", "properties": {"content": "Alec"}},
        "message": {
            "name": "message",
            "type": "text",
            "properties": {"content": "Happy birthday, Alec! Wishing you a fantastic day."},
        },
    },
}
﻿

# API Request
response = requests.post(generate_url, json=payload, headers=headers)
﻿

# Handle Response
if response.status_code == 200:
    video_data = response.json()
    print("Video URL:", video_data["video_url"])
else:
    print("Error:", response.json())
```

﻿

**Steps to Follow:**

1. Replace YOUR\_API\_KEY with your API key (found under **Settings > API** in your HeyGen account).

2. Replace YOUR\_TEMPLATE\_ID with your Template ID from Step 2.

3. Customize the name and message fields in the payload.

4. Run the script to generate the video. The video URL will appear in the response.

﻿

## **Step 4: Add OpenAI for Dynamic Script Creation**

Integrating OpenAI allows you to generate unique scripts for each video, making the content even more personalized.

### **Python Example with OpenAI:**

```
import requests
import openai
﻿

# OpenAI API Key
openai.api_key = "YOUR_OPENAI_API_KEY"
﻿

# Generate Dynamic Script with OpenAI
response = openai.Completion.create(
    engine="text-davinci-003",
    prompt="Write a funny birthday message for Alec.",
    max_tokens=50,
)
dynamic_message = response.choices[0].text.strip()
﻿

# HeyGen API Details
api_key = "YOUR_API_KEY"
template_id = "YOUR_TEMPLATE_ID"
generate_url = f"https://api.heygen.com/v2/template/{template_id}/generate"
﻿

# Request Headers
headers = {"Accept": "application/json", "X-API-KEY": api_key}
﻿

# Payload with OpenAI-Generated Script
payload = {
    "title": "Dynamic Birthday Greeting",
    "variables": {
        "name": {"name": "name", "type": "text", "properties": {"content": "Alec"}},
        "message": {
            "name": "message",
            "type": "text",
            "properties": {"content": dynamic_message},
        },
    },
}
﻿

# API Request
response = requests.post(generate_url, json=payload, headers=headers)
﻿

# Handle Response
if response.status_code == 200:
    video_data = response.json()
    print("Video URL:", video_data["video_url"])
else:
    print("Error:", response.json())
﻿
```

﻿

### **Steps to Follow:**

1. Replace YOUR\_OPENAI\_API\_KEY and YOUR\_API\_KEY with your respective API keys.

2. Update the OpenAI prompt for the type of message you’d like (e.g., professional, humorous).

3. Run the script to dynamically generate and personalize the video.

﻿

## **Step 5: Check Video Status and Download**

After generating the video, you can check its status and download it.

### **Code Snippet:**

```
import time
﻿

# Video Status Check
video_status_url = f"https://api.heygen.com/v1/video_status.get?video_id={video_id}"
﻿

while True:
    response = requests.get(video_status_url, headers=headers)
    status = response.json()["data"]["status"]
    if status == "completed":
        video_url = response.json()["data"]["video_url"]
        print("Video Completed! URL:", video_url)
        break
    elif status in ["processing", "pending"]:
        print("Video is still processing...")
        time.sleep(5)  # Wait for 5 seconds before checking again
    elif status == "failed":
        print("Video generation failed.")
        break
﻿
```

## **Resources and Support**

- **API Documentation:**﻿ [HeyGen API Docs](https://docs.heygen.com/) ﻿

- **Community Hub:** Join our community to ask questions, share ideas, and get inspired.

- **Contact Support:** Email us at **support@heygen.com** for technical assistance.

We hope this walkthrough empowers you to explore HeyGen’s API capabilities. Happy creating! 🎉

Like

Comments (0)

Popular

![avatar](<Base64-Image-Removed>)

Add a comment﻿

Comment

Table Of Contents

- [Step 1: Access the HeyGen API Documentation](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#wGSrnchsIv)
- [Step 2: Create a Video Template](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#L0hJ6z886T)
  - [How to Create a Template:](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#5e5FeqL_Kg)
- [Step 3: Generate Videos Using the Template API](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#HlD9iJ0N7T)
  - [Python Example:](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#nokzXNNte1)
- [Step 4: Add OpenAI for Dynamic Script Creation](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#2K-fz2OarZ)
  - [Python Example with OpenAI:](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#yEWXtyCONt)
  - [Steps to Follow:](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#QcUnsw1ic1)
- [Step 5: Check Video Status and Download](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#UPWvIQPtKo)
  - [Code Snippet:](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#ECFpEeUB4x)
- [Resources and Support](https://community.heygen.com/public/clubs/api-builders-au0/resources/how-to-use-heygens-api-a-step-by-step-walkthrough#LLdgaL32DD)

![Ads No.5. Click to open https://community.heygen.com/home/forum/boards/product-feedback-and-ideas-3gx](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/Banner-Feedback-b0503541-4e7e-488e-88c0-b42cf6ef74a3-1730400507424.png?fit=scale-down&width=345)

![Ads No.1. Click to open https://community.heygen.com/home/resources/community-spotlights-videos-of-the-month-september-2025](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/Community-videos-of-the-month-August-2025-banner-ad-ba63ac06-7f32-4fa2-a6bd-ad0c9466fb67-1758911667514.jpeg?fit=scale-down&width=345)

![Ads No.2. Click to open https://community.heygen.com/home/collections/heygen-academy-101](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/HA101-Ad-9d4dfe6d-59e2-41e8-9a5c-94f37699fdf4-1742580919605.png?fit=scale-down&width=345)

![Ads No.3. Click to open https://www.heygen.com/playbook/heygen-for-marketers-jumpstart-guide](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/Banner-ad-690-x-902-fee3baf4-f157-45dd-a284-aa49d4e50b41-1751325967390.jpeg?fit=scale-down&width=345)

![Ads No.4. Click to open https://community.heygen.com/home/resources/avatar-and-voice-shooting-tips-and-tricks](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/Banner-Avatar-best-practices-1--54bc27c0-8206-401d-af59-897918391d52-1736388759941.jpeg?fit=scale-down&width=345)

![Ads No.5. Click to open https://community.heygen.com/home/forum/boards/product-feedback-and-ideas-3gx](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/Banner-Feedback-b0503541-4e7e-488e-88c0-b42cf6ef74a3-1730400507424.png?fit=scale-down&width=345)

![Ads No.1. Click to open https://community.heygen.com/home/resources/community-spotlights-videos-of-the-month-september-2025](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/Community-videos-of-the-month-August-2025-banner-ad-ba63ac06-7f32-4fa2-a6bd-ad0c9466fb67-1758911667514.jpeg?fit=scale-down&width=345)

![Ads No.2. Click to open https://community.heygen.com/home/collections/heygen-academy-101](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/HA101-Ad-9d4dfe6d-59e2-41e8-9a5c-94f37699fdf4-1742580919605.png?fit=scale-down&width=345)

![Ads No.3. Click to open https://www.heygen.com/playbook/heygen-for-marketers-jumpstart-guide](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/Banner-ad-690-x-902-fee3baf4-f157-45dd-a284-aa49d4e50b41-1751325967390.jpeg?fit=scale-down&width=345)

![Ads No.4. Click to open https://community.heygen.com/home/resources/avatar-and-voice-shooting-tips-and-tricks](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/Banner-Avatar-best-practices-1--54bc27c0-8206-401d-af59-897918391d52-1736388759941.jpeg?fit=scale-down&width=345)

![Ads No.5. Click to open https://community.heygen.com/home/forum/boards/product-feedback-and-ideas-3gx](https://cdn.gradual.com/images/https://d2xo500swnpgl1.cloudfront.net/uploads/heygen/Banner-Feedback-b0503541-4e7e-488e-88c0-b42cf6ef74a3-1730400507424.png?fit=scale-down&width=345)

## Popular

[Read more about 'HeyGen API developer hub'](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-developer-hub-2024-12-11)

external

[HeyGen API developer hub](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-developer-hub-2024-12-11)

Dive in

## Related

[Read more about 'HeyGen API Feature Request Board'](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-feature-request-board-2025-05-07)

external

[HeyGen API Feature Request Board](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-feature-request-board-2025-05-07)

May 7th, 2025 • Views 57

[Read more about 'Winning projects from the HeyGen Hackaton: December 2024'](https://community.heygen.com/public/clubs/api-builders-au0/externals/winning-projects-from-the-heygen-hackaton-december-2024-2024-12-18)

external

[Winning projects from the HeyGen Hackaton: December 2024](https://community.heygen.com/public/clubs/api-builders-au0/externals/winning-projects-from-the-heygen-hackaton-december-2024-2024-12-18)

Dec 18th, 2024 • Views 554

[Read more about 'HeyGen MCP Server is live!'](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-mcp-server-is-live-2025-04-17)

external

[HeyGen MCP Server is live!](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-mcp-server-is-live-2025-04-17)

Apr 17th, 2025 • Views 74

[Read more about 'HeyGen API Postman collection'](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-postman-collection-2024-12-20)

external

[HeyGen API Postman collection](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-postman-collection-2024-12-20)

Dec 20th, 2024 • Views 217

[Read more about 'HeyGen API Feature Request Board'](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-feature-request-board-2025-05-07)

external

[HeyGen API Feature Request Board](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-feature-request-board-2025-05-07)

May 7th, 2025 • Views 57

[Read more about 'HeyGen MCP Server is live!'](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-mcp-server-is-live-2025-04-17)

external

[HeyGen MCP Server is live!](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-mcp-server-is-live-2025-04-17)

Apr 17th, 2025 • Views 74

[Read more about 'HeyGen API Postman collection'](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-postman-collection-2024-12-20)

external

[HeyGen API Postman collection](https://community.heygen.com/public/clubs/api-builders-au0/externals/heygen-api-postman-collection-2024-12-20)

Dec 20th, 2024 • Views 217

[Read more about 'Winning projects from the HeyGen Hackaton: December 2024'](https://community.heygen.com/public/clubs/api-builders-au0/externals/winning-projects-from-the-heygen-hackaton-december-2024-2024-12-18)

external

[Winning projects from the HeyGen Hackaton: December 2024](https://community.heygen.com/public/clubs/api-builders-au0/externals/winning-projects-from-the-heygen-hackaton-december-2024-2024-12-18)

Dec 18th, 2024 • Views 554

We use cookies 🍪 for analytics and to provide better services. [Learn more.](https://gradual.notion.site/Privacy-Policy-ccec78687fb44226974049ec5ed39683)

Got it

[Terms of Service](https://www.heygen.com/terms)

[Privacy Policy](https://www.heygen.com/policy)

[Code of Conduct](https://www.heygen.com/community-code-of-conduct)

[Powered by Gradual](https://www.gradual.com/?utm_source=heygen&utm_campaign=poweredByLink&utm_medium=gradual)

Twitter Widget Iframe