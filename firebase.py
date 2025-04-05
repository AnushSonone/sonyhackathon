import firebase_admin
from firebase_admin import credentials, firestore, storage

# 1) initialize firebase
SERVICE_ACCOUNT_PATH = "path/to/serviceAccountKey.json"
cred = credentials.Certificate(SERVICE_ACCOUNT_PATH)

# NOTE:
# Typically, the default bucket name is <project-id>.appspot.com,
# so here we use "sonyaitrios.appspot.com".
# If your console shows a different bucket name, replace this string.
firebase_admin.initialize_app(cred, {
    "storageBucket": "sonyaitrios.appspot.com"
})

db = firestore.client()
bucket = storage.bucket()

def upload_driver_license_image(user_id: str, image_local_path: str) -> str:
    """
    Upload a driver's license image to Firebase Storage and return its gs:// path.
    """
    blob = bucket.blob(f"driver_licenses/{user_id}.jpg")
    blob.upload_from_filename(image_local_path)

    # return the gs:// path (or store a download URL)
    gs_path = f"gs://{bucket.name}/driver_licenses/{user_id}.jpg"
    return gs_path

def save_user_license_info(user_id: str, license_image_path: str):
    """
    Save the user's license image reference in Firestore.
    """
    doc_ref = db.collection("locals").document(user_id)
    doc_ref.set({
        "license_image": license_image_path,
        "verified": False
    }, merge=True)

def main():
    # example
    user_id = "alice123"
    local_image_path = "alice_driver_license.jpg"

    # 2) upload the driver license image
    gs_path = upload_driver_license_image(user_id, local_image_path)

    # 3) store reference in Firestore
    save_user_license_info(user_id, gs_path)

    # 4) retrieve and print the firestore document
    doc_ref = db.collection("locals").document(user_id)
    doc_snapshot = doc_ref.get()
    if doc_snapshot.exists:
        print("Firestore Document:", doc_snapshot.to_dict())
    else:
        print(f"No document found for user: {user_id}")

if __name__ == "__main__":
    main()
