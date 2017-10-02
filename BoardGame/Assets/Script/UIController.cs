using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class UIController : MonoBehaviour {
	public static bool result = false;
	public GameObject button;
	public Text text;

	void Start () {
		text.enabled = false;
		button.SetActive (false);
	}
		
	void Update () {
		if (result) {
			text.enabled = true;
			button.SetActive(true);
		}
	}
}
