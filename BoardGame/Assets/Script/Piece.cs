using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Piece : MonoBehaviour {
	
	private const int WHITE_PLAYER = 0;	
	private const int BLACK_PLAYER = -1;

	private Rigidbody rigidbody;
	private int pieceOwner;
	private int positionX = -1;
	private int positionY = -1;

	public void Start(){
		rigidbody = GetComponent<Rigidbody> ();
	}
		
	public void reversePiece(){
		this.pieceOwner = ~pieceOwner;
	}

	public void setPosition(int x, int y){
		this.positionX = x;
		this.positionY = y;
	}

	public int getPositionX(){
		return positionX;
	}

	public int getPositionY(){
		return positionY;
	}

	public void setOwner(int playerColor){
		pieceOwner = playerColor;
	}

	public int getOwner(){
		return pieceOwner;
	}


	public void flipPiece(){
//		rigidbody.MoveRotation (Quaternion.AngleAxis (180, Vector3.left));
		rigidbody.AddForce (Vector3.up * 345);
		rigidbody.AddTorque (0, 0, 5);
	}
		

//	public IEnumerator flipPiece()
//	{
//		rigidbody.useGravity = false;
//		while (rigidbody.position.y < 2)
//		{
//			rigidbody.AddForce (Vector3.up * 50 * (2 - rigidbody.position.y));
//			//rigidbody.AddForce (Vector3.up * 560);
//			yield return new WaitForSeconds(.05f);
//		}
//		yield return new WaitForSeconds(.15f);
//
//		//rigidbody.AddForce (Vector3.up * 100);
//		rigidbody.AddTorque (0, 0, 8);
//		rigidbody.useGravity = true;
//	}


	private bool isTriggered = false;
	private void OnTriggerEnter(Collider other){
		if (isTriggered == false) {
			if (other.gameObject.CompareTag ("GameBoard")) {
				Debug.Log ("trigger enter : " + positionX + ", " + positionY);
				BoardManager.controllStatus = false;
			}
			isTriggered = true;
		}
	}
}
