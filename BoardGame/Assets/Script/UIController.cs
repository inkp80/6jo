using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIController : MonoBehaviour {
	public static bool result = false;
	public GameObject returyButton;
	public Text resultText;
	public Text pauseText;

	void Start () {
		pauseText.enabled = false;
		resultText.enabled = false;
		returyButton.SetActive (false);
	}
		
	void Update () {
		if (result) {
			resultText.enabled = true;
			returyButton.SetActive(true);
		}
	}
}
