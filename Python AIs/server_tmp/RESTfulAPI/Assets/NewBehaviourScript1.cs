using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using UnityEngine.Networking;

public class NewBehaviourScript1 : MonoBehaviour {
	
	public Text plainText;

	// Use this for initialization
	void Start () {
	}
	
	// Update is called once per frame
	void Update () {
		
	}

	public void getAPI(){
		plainText.text = "aaaa";
		noOption ();
	}
		

	public void noOption(){
		string url = "http://0.0.0.0:5009/post";
		WWWForm form = new WWWForm();
		form.AddField("title", "result is return");
		WWW www = new WWW (url, form);
		StartCoroutine(WaitForRequest(www));
	}


	IEnumerator WaitForRequest(WWW www)
	{
		yield return www;

		if (www.error == null)
		{
			// request completed!
			Debug.Log (www.text);
		}
		else
		{
			// something wrong!
			Debug.Log ("WWW error: " + www.error);
		}
	}
}
