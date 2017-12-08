using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class CameraController : MonoBehaviour {
	Camera main_cam;
	Quaternion basic_rotation;
	Vector3 basic_position;
	public Text cameraStateText;
	private bool cameraMovePermission = false;
	public Transform m_kTarget;
	public Transform m_basic;
	public float  m_fDistance = 10.0f;
	public float  m_fxSpeed = 250.0f;
	public float  m_fySpeed = 120.0f;

	public float  m_fyMinLimit = -20f;
	public float  m_fyMaxLimit = 80f;

	private float x = 0.0f;
	private float y = 0.0f;

	// Use this for initialization
	void Start () {
		main_cam = Camera.main;
		basic_position = main_cam.gameObject.transform.position;
		basic_rotation = main_cam.gameObject.transform.rotation;

		cameraStateText.enabled = false;
		Vector3 angles = transform.eulerAngles;
		x = angles.y;
		y = angles.x;

		// Make the rigid body not change rotation
		if (GetComponent<Rigidbody>())
			GetComponent<Rigidbody>().freezeRotation = true;
	}

	// Update is called once per frame
	public void Update () {

	}

	public void LateUpdate()
	{
		if (cameraMovePermission == false) {
			transform.rotation = basic_rotation;
			transform.position = basic_position;
			Debug.Log ("cam state : " + cameraMovePermission);
			return;
		}
		print ("lateUpdate");
		x += Input.GetAxis("Mouse X") * m_fxSpeed * 0.02f;
		y -= Input.GetAxis("Mouse Y") * m_fySpeed * 0.02f;

		y = ClampAngle(y, m_fyMinLimit, m_fyMaxLimit);

		Quaternion rotation = Quaternion.Euler(y, x, 0);
		Vector3 position = transform.position;
		if (m_kTarget) {
			position = rotation * new Vector3(0.0f, 0.0f, -m_fDistance);
			position += m_kTarget.position;

		}
		else
		{
			if (Input.GetKey(KeyCode.W))
			{
				position += (rotation * new Vector3(0.0f, 0.0f, 0.05f));
			}
			if(Input.GetKey(KeyCode.S))
			{
				position += (rotation * new Vector3(0.0f, 0.0f, -0.05f));
			}
			if(Input.GetKey(KeyCode.D))
			{
				position += (rotation * new Vector3(0.05f, 0.0f, 0));
			}
			if(Input.GetKey(KeyCode.A))
			{
				position += (rotation * new Vector3(-0.05f, 0.0f, 0));
			}

		}
		transform.rotation = rotation;
		transform.position = position;
	}
	public float ClampAngle (float angle ,float min,  float max) {
		if (angle < -360)
			angle += 360;
		if (angle > 360)
			angle -= 360;
		return Mathf.Clamp (angle, min, max);
	}

	public void OnMouseDrag(){
		Vector3 worldPoint = Input.mousePosition;
		worldPoint.z = 10;
	}

	public void changeCameraMovePermission() {
		cameraMovePermission = !cameraMovePermission;
		if (cameraMovePermission == true) {
			cameraStateText.enabled = true;
			transform.rotation = basic_rotation;
			transform.position = basic_position;
		} else {
			cameraStateText.enabled = false;
		}
		Debug.Log ("cam state : " + cameraMovePermission);
		print ("cam state : " + cameraMovePermission);
	}

}
