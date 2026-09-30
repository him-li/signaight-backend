# flake8: noqa
import pytest
import pendulum


@pytest.fixture
def profile_with_post_no_extreme_sports():
    return {
        "posts": [
            {
                "fb_post_photo": {
                    "fb_photo_id": "10218275868221597",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/e/ac/268fd/eac268fd-4d53-4521-81be-bc03cdad84c9.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
            {
                "fb_uploaded_photo": {
                    "fb_photo_likes_count": 37,
                    "fb_photo_reactions_count": 37,
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/8/4e/93d49/84e93d49-de42-45ba-b7a0-74ed9b9cf7ff.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10218275868221597",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/e/ac/268fd/eac268fd-4d53-4521-81be-bc03cdad84c9.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
            {
                "fb_uploaded_photo": {
                    "fb_photo_likes_count": 37,
                    "fb_photo_reactions_count": 37,
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/8/4e/93d49/84e93d49-de42-45ba-b7a0-74ed9b9cf7ff.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10218275868221597",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/e/ac/268fd/eac268fd-4d53-4521-81be-bc03cdad84c9.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
            {
                "fb_uploaded_photo": {
                    "fb_photo_likes_count": 37,
                    "fb_photo_reactions_count": 37,
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/8/4e/93d49/84e93d49-de42-45ba-b7a0-74ed9b9cf7ff.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
        ]
    }


@pytest.fixture
def profile_without_posts():
    return {
        "posts": None
    }


@pytest.fixture
def profile_with_posts_empty():
    return {
        "posts": []
    }


@pytest.fixture
def profile_with_posts_extreme_sports():
    return {
        "posts": [
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/c/06/b5272/c06b5272-e7bf-43be-b4e4-fb00fc25bcb5.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10222190143716038",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/63/597fb/663597fb-de66-4035-8817-8550706e8c73.jpg",
                        "width": 960,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10218275868221597",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/ae/66654/6ae66654-37dc-4767-b101-4d75ab30c136.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10222190143716038",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/63/597fb/663597fb-de66-4035-8817-8550706e8c73.jpg",
                        "width": 960,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10218275868221597",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/ae/66654/6ae66654-37dc-4767-b101-4d75ab30c136.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10222190143716038",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/63/597fb/663597fb-de66-4035-8817-8550706e8c73.jpg",
                        "width": 960,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10218275868221597",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/ae/66654/6ae66654-37dc-4767-b101-4d75ab30c136.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10222190143716038",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/63/597fb/663597fb-de66-4035-8817-8550706e8c73.jpg",
                        "width": 960,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10218275868221597",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/ae/66654/6ae66654-37dc-4767-b101-4d75ab30c136.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10222190143716038",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/63/597fb/663597fb-de66-4035-8817-8550706e8c73.jpg",
                        "width": 960,
                        "height": 960
                    }
                }
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10218275868221597",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/ae/66654/6ae66654-37dc-4767-b101-4d75ab30c136.jpg",
                        "width": 960,
                        "height": 720
                    }
                }
            },
        ]
    }


@pytest.fixture
def profile_with_post_with_sociable_events():
    return {
        "posts": [
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
        ]
    }


@pytest.fixture
def profile_with_post_no_sociable_events():
    return {
        "posts": [
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/6/ae/66654/6ae66654-37dc-4767-b101-4d75ab30c136.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
        ]
    }


@pytest.fixture
def profile_with_anti_israel():
    return {
        "posts": [
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/5/12/ef8ce/512ef8ce-2035-43f4-a728-611fdb2bdfdf.jpg",
                        "width": 720,
                        "height": 960
                    }
                },
                "fb_post_text": "Anti Israel",
                "post_author": {
                    "fb_profile_url": "https://facebook.com/123456789/",
                    "fb_user_id": "123456789"
                },
                "linkedin_post_publishment_date": "2024-05-05",
                "activity_type": "post"
            },
        ],
        "network_signature": {
            "url": {
                "facebook_profile_url": ["https://facebook.com/123456789/"]
            },
            "user_id": {
                "facebook_user_id": ["123456789"]
            }
        }
    }


@pytest.fixture
def profile_not_anti_israel():
    return {
        "posts": [
            {
                "linkedin_post_text": "I’m happy to share that I’m starting a new position as Director at ADHDoTECH!",
                "linkedin_post_publishment_date": "2026-01-27T13:07:01.833Z",
                "linkedin_post_comments_count": 16,
                "linkedin_post_likes_count": 75,
                "linkedin_post_shares_count": 0,
                "linkedin_post_url": "https://www.linkedin.com/feed/update/urn:li:activity:7421901550211547136",
                "reactions": [
                    {
                        "linkedin_post_reaction_type": "LIKE",
                        "linkedin_post_reaction_type_count": 56
                    },
                    {
                        "linkedin_post_reaction_type": "PRAISE",
                        "linkedin_post_reaction_type_count": 16
                    },
                    {
                        "linkedin_post_reaction_type": "EMPATHY",
                        "linkedin_post_reaction_type_count": 3
                    }
                ],
                "post_reaction": {
                    "reaction_type": "LIKE",
                    "reaction_target": "Post"
                },
                "post_author": {
                    "title": "Strategic Startup Advisor | Entrepreneurship Lecturer | Growth & Business Development | Co-Creator @ TheEcosystem",
                    "linkedin_profile_picture": "s3://signaight-dev/profile_photos/5/c9/44267/5c944267-cdd0-4a33-9351-c4b120746438.jpg",
                    "linkedin_profile_url": "https://linkedin.com/in/doronsimhi",
                },
                "tagged_profiles": [],
                "activity_type": "reaction"
            },
            {
                "linkedin_post_text": "This is my land. My Israel.  \nA place where Muslims, Christians, Jews, Hindus—celebrate Hanukkah, Christmas, Eid, and Diwali, side by side.\n\nUnder golden lights and open skies, we join together in solidarity, joy, and mutual respect.  \nFrom sweet cotton candy moments (my personal weakness 🥰) to the powerful glow of the Baháʼí Gardens, this is the real Israel I love — vibrant, diverse, and united.\n\nYou may not see this harmony in the news headlines,  \nbut we live it.  \nEvery day.  \n🕯️✨🕊️🇮🇱🎄🕎",
                "linkedin_post_publishment_date": "2026-01-18T20:35:10.360Z",
                "linkedin_post_comments_count": 3,
                "linkedin_post_likes_count": 91,
                "linkedin_post_shares_count": 1,
                "linkedin_post_url": "https://www.linkedin.com/feed/update/urn:li:activity:7408205636683071488",
                "reactions": [
                    {
                        "linkedin_post_reaction_type": "LIKE",
                        "linkedin_post_reaction_type_count": 77
                    },
                    {
                        "linkedin_post_reaction_type": "EMPATHY",
                        "linkedin_post_reaction_type_count": 9
                    },
                    {
                        "linkedin_post_reaction_type": "APPRECIATION",
                        "linkedin_post_reaction_type_count": 5
                    }
                ],
                "post_reaction": {
                    "reaction_type": "LIKE",
                    "reaction_target": "Post"
                },
                "post_author": {
                    "title": "Israel Country Manager and Business Operation Manager IFM, Global Occupier Services at Cushman & Wakefield",
                    "linkedin_profile_picture": "s3://signaight-dev/profile_photos/7/61/bc562/761bc562-3b6f-464f-8979-e13f7a3facbc.jpg",
                    "linkedin_profile_url": "https://linkedin.com/in/keren-maoz-21214110",
                },
                "tagged_profiles": [],
                "activity_type": "reaction"
            },
            {
                "linkedin_post_text": "שנה פלוס.\nשנה פלוס מאז שחזרתי לעבוד באופן עצמאי לגמרי.\nשנה של מאמצים עילאיים לדחוף את העשייה שלי קדימה, להתפרנס בכבוד, ולנסות לבנות חיים שיש בהם גם משמעות.\nזו הייתה שנה גדושה ביצירתיות, התלהבות, למידה ועשייה.\nהצלחתי להתפרנס מהעסק יותר מבכל שנה אחרת שבה עבדתי גם כעצמאית וגם כשכירה –\nאבל בסך הכול לא הגעתי לאותה רמת הכנסה.\n\nאז האם זו הצלחה או כישלון?\n\nלפי הקפיטליזם – התשובה ברורה.\nאבל אני לא לגמרי במטריקס. בשבילי כסף הוא האמצעי, לא המטרה. המטרה שלי היא לעשות משהו שאני נהנית ממנו ושמועיל לעולם. (יש כמה ארגונים מובילים שפועלים לפי העיקרון הזה - כמו פטגוניה).\n\nאז מה בעצם קרה בשנה הזו?\n\nבניתי עוד זרוע מקצועית: ייעוץ לסימביוזה תעשייתית.\nקידמתי עסקאות עם חברות בארץ ובעולם, חלקן הבשילו לכדי שיתופי פעולה ממשיים. המשמעותית שבהן – חיבור בין חברת תרופות לחברת דשנים (כן, זה דווקא כן קיימי).\nבמקביל התחלתי לשלב יותר ויותר בינה מלאכותית בעבודה, וגם בניתי את ״רעות״ – סוכנת סימביוזה תעשייתית שיכולה לסייע בחינם במציאת פתרונות לפסולת.\n\nבעיינה המשכנו ללוות עסקים בהטמעת קיימות, כולל שני פרויקטים משמעותיים של רכש בר־קיימא, והפקנו שני קורסים על שוק הפחמן בהובלתה של מיכל וולנסקי האדירה. זה היה פרויקט אינטנסיבי ומורכב, ואני גאה בו מאוד.\n\nובמקביל המשכתי להעביר הרצאות\nהאחרונה שבהן הייתה עבורי אחד השיאים של העשור האחרון. אני מנועה מלציין את שם הארגון או הסקטור, אבל רוצה לספר על היום השלם שבניתי והעברתילהם, על מבוא לקיימות. זוהי קומפילציה של שנים של ניסיון, חשיבה ועבודה קשה.\nארבע הרצאות שבונות זו על זו:\nמבוא לקיימות,\nניתוח עומק של הסקטור והמגמות המרכזיות בו בנושאי קיימות,\nמשבר החומרים וכלכלה מעגלית,\nולבסוף – עקרונות הקיימות ככלי מועיל ויישומי להטמעת קיימות \nהפידבק היה ממש טוב. אם בעבר תהיתי האם אני באמת מרצה שיודעת גם לעניין וגם להעביר מסרים מורכבים – היום אני כבר יודעת שכן. זו אבן דרך שאני שמחה ומתרגשת שהגעתי אליה.\nתודה Michal Greenspan-Tamam על ההזדמנות.\n\nבחודשים האחרונים חלה תמורה: חזרתי לשלב בין עבודה כשכירה לעצמאית, ולכן גם השקט היחסי ברשתות. בהמשך אשתף על המשרה.\nבינתיים אני מנסה להנדס מחדש את חיי, עם ילדה מתוקה שהפכה להיות מרכז חיי המופלא, וזוגיות טובה שאני מברכת עליה כל יום. \n\nבעיקר אני רוצה להגיד תודה.\nתודה ל Hagar Lidor שותפתי היקרה, על העשור האחרון והשותפות הנדירה שלנו.\nתודה ל Michal Volansky המלכה' שהצטרפת אלינו לעיינה והפקת והובלת את הקורסים שלנו על שוק הפחמן.\nתודה לאהובי Ishay Mamluk , השותף השקט, המאמן האישי והחבר הכי טוב שלי.\nתודה לליבי, ילדתי היקרה מכל, שפיצצת את ליבי באהבה ושמחה ללא סוף, ולאבא של ליבי, ניצן שמגדל אותך יחד איתי באהבה אין קץ.\nתודה למשפחה שלי בדם ובנפש, לכל האחיות והאחים שלי.\nתודה לכל השותפות והשותפים לתחום הקיימות.\nותודה לכל הלקוחות שלי שנתנו בי אמון וצעדו איתי כברת דרך.\n\n2026 - מקווה שתהיי שנת שינוי לטובה, גם ברמת המדינה וגם ברמה האישית והמקצועית!\n\nבתמונה - החיבור בין קפיטליזם לקיימות (:",
                "linkedin_post_publishment_date": "2026-01-15T21:06:08.701Z",
                "linkedin_post_comments_count": 19,
                "linkedin_post_likes_count": 62,
                "linkedin_post_shares_count": 0,
                "linkedin_post_url": "https://www.linkedin.com/feed/update/urn:li:activity:7417498584671064064",
                "reactions": [
                    {
                        "linkedin_post_reaction_type": "LIKE",
                        "linkedin_post_reaction_type_count": 50
                    },
                    {
                        "linkedin_post_reaction_type": "EMPATHY",
                        "linkedin_post_reaction_type_count": 8
                    },
                    {
                        "linkedin_post_reaction_type": "PRAISE",
                        "linkedin_post_reaction_type_count": 3
                    },
                    {
                        "linkedin_post_reaction_type": "APPRECIATION",
                        "linkedin_post_reaction_type_count": 1
                    }
                ],
                "post_reaction": {
                    "reaction_type": "LIKE",
                    "reaction_target": "Post"
                },
                "post_author": {
                    "title": "Founding partner at Ayana - Strategic Sustainability consultancy | Lecturer for Sustainability | Industrial Symbiosis expert | Project Manager | Vipassana Practitioner",
                    "linkedin_profile_picture": "s3://signaight-dev/profile_photos/4/58/1e9f0/4581e9f0-2393-4acb-9d83-c4f29484bb61.jpg",
                    "linkedin_profile_url": "https://linkedin.com/in/hilashapira",
                },
                "tagged_profiles": [],
                "activity_type": "reaction"
            },
            {
                "linkedin_post_text": "“משבר תשתיות הוא תמיד קודם כול משבר של אנשים.”\n\nביום שישי האחרון השתתפתי בכינוס המועצה ההנדסית של התאגדות מהנדסי החשמל, האלקטרוניקה והאנרגיה בישראל -\n“בין עתודה הנדסית לעלטה חשמלית” - וישבתי סביב שולחן אחד עם כ-50 מהאנשים שמעצבים בפועל את עתיד משק החשמל והאנרגיה בישראל.\nבכירי האקדמיה והתעשייה.\n\nלהיות חבר במועצה ההנדסית, עבורי, זו לא שורה בקורות החיים.\nזו שליחות.\nזו הזכות - והאחריות - להיות חלק מהשיח שבו מתקבלות החלטות שמשפיעות על דור שלם של מהנדסים ועל תשתיות שמחזיקות מדינה.\n\nהתכנסנו כדי לנתח אירועי עלטה.\nאבל מהר מאוד היה ברור - זה לא אירוע נקודתי. זה תמרור אזהרה.\n\nכי מאחורי כל מערכת, כל רשת וכל תשתית - עומדים אנשים.\nוהשאלה האמיתית היא:\nהאם תהיה לנו עתודה הנדסית מספיק חזקה להחזיק את משק החשמל והאנרגיה בעשור הבא.\n\nככל שהדיון העמיק, התובנה המרכזית התחדדה:\nהאתגר שלנו הוא לא רק טכנולוגי. הוא קודם כול אנושי.\n\nוזה נראה כך בפועל:\n\n🔹 דור העתיד לא יגיע לבד - צריך להבין אותו, לדבר בשפה שלו ולהירתם אליו. זו הזדמנות אמיתית לשינוי.\n🔹 הכשרה מקצועית והכנת עתודה הנדסית הן אחריות לאומית, לא יוזמה נקודתית. נדרשת תכנית סדורה, ארוכת טווח.\n🔹 פיתוח סגל אקדמי בכיר וחזק שמחובר לאתגרי המשק ומגדל מצוינות לאורך זמן.\n🔹 הצבת המובילים הצעירים בקדמת הבמה - עם משאבים, תקנים, אמון והשפעה כבר היום.\n🔹 השקעה בדור הצעיר משתלמת - אני רואה את זה יום-יום, גם מניסיון אישי.\n\nולצד החזון, השיח היה גם מאוד מעשי:\n\n✔️ תיקון מערך הרישוי.\n✔️ פנייה לסטודנטים כבר בשנה ב’.\n✔️ בניית תכניות הכשרה ייעודיות למשק החשמל והאנרגיה.\n✔️ גיוס תקציבים ייעודיים למחקר ופיתוח במערכות ההספק.\n\nיצאתי מהכינוס עם תחושת אחריות כבדה -\nאבל גם עם הרבה אופטימיות.\n\nיש סביב השולחן אנשים מצוינים, מחויבים, עם הבנה עמוקה של גודל השעה.\nועכשיו נדרשת ההחלטה החשובה באמת:\n\nלהשקיע בדור הבא - לא מחר, אלא עכשיו.\n\nIEC - Israel Electric Corporation חברת החשמל לישראל בע\"מ Igor Aronovich Shiki Fisher נגה - החברה לניהול מערכת החשמל Noga - Israel Independent System Operator SEEEI -התאגדות מהנדסי חשמל, אלקטרוניקה ואנרגיה בישראל - Avraham (Avi) Menashe Yuval Beck Emil Koifman Chen Baraf Yossi Ben Yakar Nayif Hino Dima Yudashkin דימה יודשקין Tel Aviv University Holon Institute of Technology SCE Sami Shamoon College of Engineering Ishay Gabay Shimon Katz Kinneret Academic College The Faculty of Engineering at Kinneret Academic College - הפקולטה להנדסה במכללה האקדמית כנרת Jerusalem College of Technology Technion - Israel Institute of Technology Ariel University Afeka Tel Aviv Academic College of Engineering Ben-Gurion University of the Negev Irit Juwiler Nissim Amos yakov(yasha) Hain HAIM DAVID Abraham Alexandrovitz \n\n#iectechstory",
                "linkedin_post_publishment_date": "2026-01-10T17:10:22.559Z",
                "linkedin_post_comments_count": 5,
                "linkedin_post_likes_count": 49,
                "linkedin_post_shares_count": 0,
                "linkedin_post_url": "https://www.linkedin.com/feed/update/urn:li:activity:7415802196379787264",
                "reactions": [
                    {
                        "linkedin_post_reaction_type": "LIKE",
                        "linkedin_post_reaction_type_count": 46
                    },
                    {
                        "linkedin_post_reaction_type": "PRAISE",
                        "linkedin_post_reaction_type_count": 2
                    },
                    {
                        "linkedin_post_reaction_type": "ENTERTAINMENT",
                        "linkedin_post_reaction_type_count": 1
                    }
                ],
                "post_reaction": {
                    "reaction_type": "LIKE",
                    "reaction_target": "Post"
                },
                "post_author": {
                    "title": "Head of Power Grid Planning and Execution Department at IEC I Distribution Unit | Chairman of the Students and Young Electrical Engineers Forum at the SEEEI Association",
                    "linkedin_profile_picture": "s3://signaight-dev/profile_photos/1/18/dc681/118dc681-78d2-46a2-b5bc-4bc5f3d80f5c.jpg",
                    "linkedin_profile_url": "https://linkedin.com/in/moshe-bibi",
                },
                "tagged_profiles": [],
                "activity_type": "reaction"
            }
        ],
        "network_signature": {
            "url": {
                "facebook_profile_url": ["https://facebook.com/123456789/"]
            },
            "user_id": {
                "facebook_user_id": ["123456789"]
            }
        }
    }


@pytest.fixture
def profile_not_anti_israel_2():
    return {
        "posts": [

            {
                "linkedin_post_text": "Smart retailers don't just gather #data, they apply it. Read the blog: #MSFTAdvocate",
                "linkedin_post_publishment_date": "2018-07-31T23:38:39.456Z",
                "linkedin_post_comments_count": 0,
                "linkedin_post_likes_count": 0,
                "linkedin_post_shares_count": 0,
                "linkedin_post_url": "https://www.linkedin.com/feed/update/urn:li:activity:6430204916215746560",
                "reactions": [],
                "post_author": {
                    "title": "Imagine, Experiment, and Adopt AI capabilities faster.",
                    "linkedin_profile_picture": "s3://signaight-dev/profile_photos/1/90/4109a/1904109a-c8eb-42cb-8cb3-e991ea21edb2.jpg",
                    "linkedin_profile_url": "https://linkedin.com/in/mikemir",
                },
                "tagged_profiles": [],
                "activity_type": "post"
            },
            {
                "linkedin_post_text": "We’re gearing up for an exciting 2026 and can’t wait to connect with you at the year’s most influential tech conferences! From #TCEA2026 and #msignite to NVIDIA’s #GTC26 and other global events, our team is ready to share insights, explore innovation, and build the future of technology together. Will you be there? Let’s make 2026 a breakthrough year!\n#TechEvents #Innovation #Networking #FutureReady #SHIEvents",
                "linkedin_post_publishment_date": "2026-01-26T15:29:08.454Z",
                "linkedin_post_comments_count": 0,
                "linkedin_post_likes_count": 9,
                "linkedin_post_shares_count": 0,
                "linkedin_post_url": "https://www.linkedin.com/feed/update/urn:li:activity:7421574925586583552",
                "reactions": [
                    {
                        "linkedin_post_reaction_type": "LIKE",
                        "linkedin_post_reaction_type_count": 9
                    }
                ],
                "post_reaction": {
                    "reaction_type": "LIKE",
                    "reaction_target": "Post"
                },
                "post_author": {
                    "title": "Manager - Product Marketing - Software Solutions",
                    "linkedin_profile_picture": "s3://signaight-dev/profile_photos/4/f9/e7ccb/4f9e7ccb-927d-4cc8-b080-5f14dbe93a4a.jpg",
                    "linkedin_profile_url": "https://linkedin.com/in/michael-brown-86b1205",
                },
                "tagged_profiles": [],
                "activity_type": "reaction"
            }

        ]
    }


@pytest.fixture
def profile_without_anti_israel():
    return {
        "posts": [
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                },
                "fb_post_text": "Love Israel"
            }
        ]
    }


@pytest.fixture
def profile_fb_post_text_no_altruism():
    return {
        "posts": [
            {
                "fb_post_text": "build bridge"
            },
            {
                "fb_post_text": "build bridge"
            },
            {
                "fb_post_text": "build bridge"
            },
        ]
    }


@pytest.fixture
def profile_with_anti_usa():
    return {
        "posts": [
            {
                "fb_post_text": "Anti USA, don't like USA, hate and destroy USA",
                "post_author": {
                    "fb_profile_url": "https://facebook.com/123456789/",
                    "fb_user_id": "123456789"
                },
                "linkedin_post_publishment_date": "2024-05-05"
            },
        ],
        "network_signature": {
            "url": {
                "facebook_profile_url": ["https://facebook.com/123456789/"]
            },
            "user_id": {
                "facebook_user_id": ["123456789"]
            }
        }
    }


@pytest.fixture
def profile_without_anti_usa():
    return {
        "posts": [
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/9/63/cbeaf/963cbeaf-5ac5-4b59-861c-0fa307774609.jpg",
                        "width": 720,
                        "height": 960
                    }
                },
                "fb_post_text": "Love USA"
            }
        ]
    }


@pytest.fixture
def profile_fb_post_text_altruism():
    return {
        "posts": [
            {
                "fb_post_text": "save children"
            },
            {
                "fb_post_text": "build bridge"
            },
            {
                "fb_post_text": "save children"
            },
        ]
    }


@pytest.fixture
def profile_empty_posts():
    return {
        "posts": [
        ]
    }


@pytest.fixture
def profile_fb_post_text_optimism():
    return {
        "posts": [
            {
                "fb_post_text": "great and happy days"
            },
        ]
    }


@pytest.fixture
def profile_fb_post_text_supporting_israel():
    return {
        "posts": [
            {
                "fb_post_text": "love Israel"
            },
            {
                "linkedin_post_text": "love Israel"
            },
        ]
    }


@pytest.fixture
def profile_fb_post_text_not_supporting_israel():
    return {
        "posts": [
            {
                "fb_post_text": "love birds"
            },
            {
                "linkedin_post_text": "love cats"
            },
        ]
    }


@pytest.fixture
def profile_li_post_text_team_related_3_posts():
    return {
        "posts": [
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
        ]
    }


@pytest.fixture
def profile_li_post_text_team_related_6_posts():
    return {
        "posts": [
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
        ]
    }


@pytest.fixture
def profile_li_post_text_not_team_related():
    return {
        "posts": [
            {
                "activity_type": "post",
                "linkedin_post_text": "no team"
            },
        ]
    }


@pytest.fixture
def profile_li_post_reaction_team_related_3_posts():
    return {
        "posts": [
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
        ]
    }


@pytest.fixture
def profile_li_post_reaction_team_related_6_posts():
    return {
        "posts": [
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
        ]
    }


@pytest.fixture
def profile_li_post_reaction_not_team_related():
    return {
        "posts": [
            {
                "activity_type": "reaction",
                "linkedin_post_text": "no team"
            },
        ]
    }


@pytest.fixture
def profile_li_posts_and_reactions_team_related_6_posts():
    return {
        "posts": [
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "reaction",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
            {
                "activity_type": "post",
                "linkedin_post_text": "Great team building activity"
            },
        ]
    }


@pytest.fixture
def profile_li_post_jihadist_text():
    return {
        "posts": [
            {
                "linkedin_post_text": "أنغماسي"
            },
        ]
    }


@pytest.fixture
def profile_li_post_salafist_text():
    return {
        "posts": [
            {
                "linkedin_post_text": "جهاد"
            },
        ]
    }


@pytest.fixture
def profile_li_post_no_extreme_text():
    return {
        "posts": [
            {
                "linkedin_post_text": "Great team building activity"
            },
        ]
    }


@pytest.fixture
def profile_fb_6_post_jihadist_text():
    return {
        "posts": [
            {
                "fb_post_text": "أنغماسي"
            },
            {
                "fb_post_text": "أنغماسي"
            },
            {
                "fb_post_text": "أنغماسي"
            },
            {
                "fb_post_text": "أنغماسي"
            },
            {
                "fb_post_text": "أنغماسي"
            },
            {
                "fb_post_text": "أنغماسي"
            },
        ]
    }


@pytest.fixture
def profile_fb_post_salafist_text():
    return {
        "posts": [
            {
                "fb_post_text": "جهاد"
            },
        ]
    }


@pytest.fixture
def profile_fb_post_no_extreme_text():
    return {
        "posts": [
            {
                "fb_post_text": "Great team building activity"
            },
        ]
    }


@pytest.fixture
def profile_instagram_post_jihadist_text():
    return {
        "posts": [
            {
                "instagram_post_text": "أنغماسي"
            },
        ]
    }


@pytest.fixture
def profile_instagram_3_post_salafist_text():
    return {
        "posts": [
            {
                "instagram_post_text": "جهاد"
            },
            {
                "instagram_post_text": "جهاد"
            },
            {
                "instagram_post_text": "جهاد"
            },
        ]
    }


@pytest.fixture
def profile_instagram_post_jihadist_text_non_arabic_term():
    return {
        "posts": [
            {
                "instagram_post_text": "Inghimasi"
            },
        ]
    }


@pytest.fixture
def profile_instagram_3_post_salafist_text_non_arabic_term():
    return {
        "posts": [
            {
                "instagram_post_text": "Jihad"
            },
            {
                "instagram_post_text": "Jihad"
            },
            {
                "instagram_post_text": "- Jihad "
            },
        ]
    }


@pytest.fixture
def profile_instagram_post_no_extreme_text():
    return {
        "posts": [
            {
                "instagram_post_text": "Great team building activity"
            },
        ]
    }


@pytest.fixture
def profile_instagram_post_weapons():
    return {
        "posts": [
            {
                "instagram_post_photo": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg"
            },
        ]
    }


@pytest.fixture
def profile_linkedin_post_weapons():
    return {
        "posts": [
            {
                "linkedin_post_photo": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg"
            },
        ]
    }


@pytest.fixture
def profile_fb_post_weapons():
    return {
        "posts": [
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg",
                        "width": 720,
                        "height": 960
                    }
                }
            },
        ]
    }


@pytest.fixture
def profile_post_weapons():
    return {
        "posts": [
            {"fb_post_text": "weapons", "activity_type": "post"},
            {"fb_post_text": "kitchen", "activity_type": "post"},
            {
                "instagram_post_photo": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg",
                "activity_type": "post"
            },
            {
                "linkedin_post_photo": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg",
                "activity_type": "post"
            },
            {
                "fb_post_photo": {
                    "fb_photo_id": "10214694055798525",
                    "fb_photo": {
                        "url": "s3://signaight-dev/profile_photos/1/93/00549/19300549-2678-4cd4-8f80-74389963fab5.jpg",
                        "width": 720,
                        "height": 960,
                    },
                },
                "activity_type": "post"
            },
        ]
    }


@pytest.fixture
def profile_fb_post_salafist_text_english():
    return {
        "posts": [
            {
                "fb_post_text": "Al Kufr Bit Taghut — [1 CONDITION/PILLAR OF TAWHEED]. Do you know how to reject the taghut in order for your Islam to be valid?. (The one who loves the kuffar (disbelievers) does not have eemaan (belief) in his heart and is a disbeliever like them, even if this kaffir was their own blood, father, brother)"
            },
        ]
    }


@pytest.fixture
def profile_fb_post_islamist_text_english():
    return {
        "posts": [
            {
                "fb_post_text": "jihaad"
            },
        ]
    }


@pytest.fixture
def profile_instagram_post_intagram_bio_multiple_salafist_text():
    return {
        "posts": [
            {
                "instagram_post_text": "Shaykh Ibn al Uthaymin رحمه الله said:\n\n“And we believe that there is a difference between a person who legislates laws which oppose the Shari’a so that he may judge between the people by it, and another person who judges by other than what Allah revealed in a specific case.\n\nThat is because the one who legislates laws so that the people follow it while knowing of it’s opposition to the Shari’a but he wishes for the people to be upon that, is a kafir.\n\nbut one who rules (by other than what Allah revealed) in a specific case while knowing the hukm of Allah in that case but due to a desire within himself (he rules by other than what Allah revealed) then he is a dhalim or a fasiq and his kufr if he is attributed to kufr is kufr duna kufr (i.e minor kufr which does not expel one from the religion).”",
                "instagram_post_photo": "s3://signaight-dev/profile_photos/7/05/6832f/7056832f-94fc-47b2-bb01-3d69a7ca9c76.jpg",
            },
        ],
        "biographic_details": {
            "description_bio_intro": {
                "instagram_bio": "هذا حساب رسمي (This is an official account)\nAthari-Hanbali\nShari’ah enthusiast \nKufr bit taghut enjoyer",
            }
        }
    }
