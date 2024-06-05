send_message_to_queue = """
{
    "type": "APPLICATION_RECORD_OF_SUBMISSION",
    "to": "notificationtest@bb.nn",
    "content": {
        "application": {
            "round_name": "",
            "last_edited": "2024-05-10T12:33:44.308109",
            "fund_id": "1e4bd8b0-b399-466d-bbd1-572171bbc7bd",
            "round_id": "50062ff6-e696-474d-a560-4d9af784e6e5",
            "reference": "HSRA-R1-JEAQRR",
            "language": "en",
            "project_name": "Need HSra fund for me",
            "started_at": "2024-05-10T12:29:29.837744",
            "id": "8be9756e-8404-4d79-9b70-abf15066845f",
            "account_id": "e38a2450-388a-40b3-92fc-1b680e3f29c9",
            "date_submitted": "2024-05-10T12:33:50.068095",
            "forms": [
                {
                    "name": "refurbishment-costs-hsra",
                    "questions": [
                        {
                            "category": "qvSwnW",
                            "question": "What is the total expected cost of refurbishment, in pounds?",
                            "fields": [
                                {
                                    "key": "pfEHzn",
                                    "title": "What is the total expected cost of refurbishment, in pounds?",
                                    "type": "text",
                                    "answer": "2"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "qvSwnW",
                            "question": "Upload the independent survey of works",
                            "fields": [
                                {
                                    "key": "SMwXcK",
                                    "title": "Upload the independent survey of works",
                                    "type": "text",
                                    "answer": "component_connection-frontend-formrunner.drawio (1).png"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "qvSwnW",
                            "question": "Upload quotes showing refurbishment costs",
                            "fields": [
                                {
                                    "key": "xUgKLI",
                                    "title": "Upload quotes showing refurbishment costs",
                                    "type": "text",
                                    "answer": "component_connection-frontend-formrunner.drawio.png"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "name-your-application-hsra",
                    "questions": [
                        {
                            "category": "CiYZae",
                            "question": "What would you like to name your application?",
                            "fields": [
                                {
                                    "key": "qbBtUh",
                                    "title": "What would you like to name your application?",
                                    "type": "text",
                                    "answer": "Need HSra fund for me"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "applicant-information-hsra",
                    "questions": [
                        {
                            "category": "bnfUAs",
                            "question": "Who should we contact about this application?",
                            "fields": [
                                {
                                    "key": "OkKkMd",
                                    "title": "Full name",
                                    "type": "text",
                                    "answer": "ee"
                                },
                                {
                                    "key": "Lwkcam",
                                    "title": "Job title",
                                    "type": "text",
                                    "answer": "ee"
                                },
                                {
                                    "key": "XfiUqN",
                                    "title": "Email address",
                                    "type": "text",
                                    "answer": "ee@ff.cc"
                                },
                                {
                                    "key": "DlZjvr",
                                    "title": "Telephone number",
                                    "type": "text",
                                    "answer": "+447588859133"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "declaration-hsra",
                    "questions": [
                        {
                            "category": "wycNzR",
                            "question": "Do you confirm all the information provided is correct?",
                            "fields": [
                                {
                                    "key": "QUaOGq",
                                    "title": "By submitting this application, you confirm that the information you
                                    have provided is correct.",
                                    "type": "list",
                                    "answer": [
                                        "confirm"
                                    ]
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "joint-applicant-hsra",
                    "questions": [
                        {
                            "category": "vpxTQD",
                            "question": "Are you making a joint application with another local authority?",
                            "fields": [
                                {
                                    "key": "luWnQp",
                                    "title": "Are you making a joint application with another local authority?",
                                    "type": "list",
                                    "answer": true
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "vpxTQD",
                            "question": "Which local authority are you applying with?",
                            "fields": [
                                {
                                    "key": "cVDqxW",
                                    "title": "Which local authority are you applying with?",
                                    "type": "text",
                                    "answer": "ee"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "vpxTQD",
                            "question": "Who from that authority should we contact about this application?",
                            "fields": [
                                {
                                    "key": "CyfqVo",
                                    "title": "Full name",
                                    "type": "text",
                                    "answer": "ee"
                                },
                                {
                                    "key": "EvfEzH",
                                    "title": "Email address",
                                    "type": "text",
                                    "answer": "ee@ff.cc"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "total-expected-cost-hsra",
                    "questions": [
                        {
                            "category": "XDldxG",
                            "question": "What is the total expected cost of delivering the HSRA, in pounds?",
                            "fields": [
                                {
                                    "key": "lfXuaP",
                                    "title": "What is the total expected cost of delivering the HSRA, in pounds?",
                                    "type": "text",
                                    "answer": "222"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "XDldxG",
                            "question": "Have you secured any match funding?",
                            "fields": [
                                {
                                    "key": "KSQYyb",
                                    "title": "Have you secured any match funding?",
                                    "type": "list",
                                    "answer": true
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "XDldxG",
                            "question": "Match funding details",
                            "fields": [
                                {
                                    "key": "QveKZm",
                                    "title": "How much match funding have you secured, in pounds?",
                                    "type": "text",
                                    "answer": "2"
                                },
                                {
                                    "key": "pyCINJ",
                                    "title": "Who is providing this?",
                                    "type": "text",
                                    "answer": "2d"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "organisation-information-hsra",
                    "questions": [
                        {
                            "category": "eaktoV",
                            "question": "Which local authority are you applying from?",
                            "fields": [
                                {
                                    "key": "WLddBt",
                                    "title": "Which local authority are you applying from?",
                                    "type": "text",
                                    "answer": "eeee"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "eaktoV",
                            "question": "Who is your section 151 officer?",
                            "fields": [
                                {
                                    "key": "okHmBB",
                                    "title": "Full name",
                                    "type": "text",
                                    "answer": "ee"
                                },
                                {
                                    "key": "bQOXTi",
                                    "title": "Email address",
                                    "type": "text",
                                    "answer": "ee@ff.cc"
                                },
                                {
                                    "key": "phaosT",
                                    "title": "Telephone number",
                                    "type": "text",
                                    "answer": "+447588859133"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "designated-area-details-hsra",
                    "questions": [
                        {
                            "category": "YFgsrH",
                            "question": "Which designated high street or town centre is the vacant property in?",
                            "fields": [
                                {
                                    "key": "frDgtU",
                                    "title": "Which designated high street or town centre is the vacant property in?",
                                    "type": "text",
                                    "answer": "e3"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "YFgsrH",
                            "question": "Where have you published the designation details?",
                            "fields": [
                                {
                                    "key": "fmWgiF",
                                    "title": "Where have you published the designation details?",
                                    "type": "text",
                                    "answer": "http://localhost:3009/"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "YFgsrH",
                            "question": "Number of commercial properties",
                            "fields": [
                                {
                                    "key": "boXxzj",
                                    "title": "How many commercial properties are in the designated area?",
                                    "type": "text",
                                    "answer": "3"
                                },
                                {
                                    "key": "eBpXPM",
                                    "title": "How many of these are vacant?",
                                    "type": "text",
                                    "answer": "3"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "other-costs-hsra",
                    "questions": [
                        {
                            "category": "qavZyX",
                            "question": "What is the total of any other expected costs, in pounds?",
                            "fields": [
                                {
                                    "key": "uJIluf",
                                    "title": "What is the total of any other expected costs, in pounds?",
                                    "type": "text",
                                    "answer": "3"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "qavZyX",
                            "question": "Upload quotes showing other costs",
                            "fields": [
                                {
                                    "key": "kRiNuO",
                                    "title": "Upload quotes showing other costs",
                                    "type": "text",
                                    "answer": "component_connection-notification-service-current.drawio.png"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "milestones-hsra",
                    "questions": [
                        {
                            "category": "wtecPW",
                            "question": "When do you expect the auction to take place?",
                            "fields": [
                                {
                                    "key": "yvpmIv",
                                    "title": "When do you expect the auction to take place?",
                                    "type": "date",
                                    "answer": "1991-06-01"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "wtecPW",
                            "question": "When do you expect to submit your claim?",
                            "fields": [
                                {
                                    "key": "gzJqwe",
                                    "title": "When do you expect to submit your claim?",
                                    "type": "date",
                                    "answer": "2035-02-02"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "wtecPW",
                            "question": "When do you expect the tenant to sign  the tenancy agreement?",
                            "fields": [
                                {
                                    "key": "ihfalZ",
                                    "title": "When do you expect the tenant to sign  the tenancy agreement?",
                                    "type": "date",
                                    "answer": "2002-03-03"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "wtecPW",
                            "question": "When do you expect to finish the refurbishment works?",
                            "fields": [
                                {
                                    "key": "fIkkRN",
                                    "title": "When do you expect to finish the refurbishment works?",
                                    "type": "date",
                                    "answer": "2002-03-03"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "wtecPW",
                            "question": "When do you expect the tenant to move in?",
                            "fields": [
                                {
                                    "key": "VoAANy",
                                    "title": "When do you expect the tenant to move in?",
                                    "type": "date",
                                    "answer": "2012-03-03"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "wtecPW",
                            "question": "When do you expect to submit your post-payment verification (PPV)?",
                            "fields": [
                                {
                                    "key": "KFjxBs",
                                    "title": "When do you expect to submit your post-payment verification (PPV)?",
                                    "type": "date",
                                    "answer": "1232-02-02"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "auction-costs-hsra",
                    "questions": [
                        {
                            "category": "ebIBcm",
                            "question": "What is the total expected cost of the auction, in pounds?",
                            "fields": [
                                {
                                    "key": "kNlEvn",
                                    "title": "What is the total expected cost of the auction, in pounds?",
                                    "type": "text",
                                    "answer": "2"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "ebIBcm",
                            "question": "Upload quotes showing auction costs",
                            "fields": [
                                {
                                    "key": "QXHlgU",
                                    "title": "Upload quotes showing auction costs",
                                    "type": "text",
                                    "answer": "component_connection-frontend-formrunner.drawio (1).png"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                },
                {
                    "name": "vacant-property-details-hsra",
                    "questions": [
                        {
                            "category": "ISBazm",
                            "question": "What is the vacant property's address?",
                            "fields": [
                                {
                                    "key": "dwLpZU",
                                    "title": "What is the vacant property's address?",
                                    "type": "text",
                                    "answer": "te, null, leeds, null, ls63es"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "ISBazm",
                            "question": "What is the total commercial floorspace of the property, in meters squared?",
                            "fields": [
                                {
                                    "key": "rFpLZQ",
                                    "title": "What is the total commercial floorspace of the property,
                                    in meters squared?",
                                    "type": "text",
                                    "answer": "3"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "ISBazm",
                            "question": "Term of vacancy",
                            "fields": [
                                {
                                    "key": "NnOqGc",
                                    "title": "How many days has the property been vacant?",
                                    "type": "text",
                                    "answer": "3"
                                },
                                {
                                    "key": "qYtKIg",
                                    "title": "How have you verified this?",
                                    "type": "freeText",
                                    "answer": "<p>e</p>"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "ISBazm",
                            "question": "Upload the initial notice you served the landlord",
                            "fields": [
                                {
                                    "key": "ndpQJk",
                                    "title": "Upload the initial notice you served the landlord",
                                    "type": "text",
                                    "answer": "1692589659464.jpeg"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": "ISBazm",
                            "question": "Before you served notice, what contact did you make with the landlord about
                            the property’s vacant status?",
                            "fields": [
                                {
                                    "key": "vAvGTE",
                                    "title": "Before you served notice, what contact did you make with the landlord
                                    about the property’s vacant status?",
                                    "type": "freeText",
                                    "answer": "<p>eee</p>"
                                }
                            ],
                            "index": 0,
                            "status": "COMPLETED"
                        },
                        {
                            "category": null,
                            "question": "MarkAsComplete",
                            "fields": [
                                {
                                    "key": "markAsComplete",
                                    "title": "Do you want to mark this section as complete?",
                                    "type": "boolean",
                                    "answer": true
                                }
                            ],
                            "status": "COMPLETED"
                        }
                    ],
                    "status": "COMPLETED"
                }
            ],
            "status": "SUBMITTED",
            "fund_name": "High Street Rental Auctions Fund"
        },
        "contact_help_email": "HighStreetRentalAuctions@levellingup.gov.uk"
    }
}
"""  # pragma: allowlist secret
