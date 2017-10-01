using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BoardManager : MonoBehaviour {
	public static bool controllStatus = true;


	private int[] dx = { 0, 1, 1, 1, 0, -1, -1, -1 };
	private int[] dy = { 1, 1, 0, -1, -1, -1, 0, 1 };

	private const int WHITE_PLAYER = 0;
	private const int BLACK_PLAYER = -1;
	private const float TILE_SIZE = 1.0f;
	private const float TILE_OFFSET = 0.5f;

	//white player : 0 (play first) / black player : -1
	private int currentPlayer = 0; 
	private int selectionX = -1;
	private int selectionY = -1;

	//추가됨. 8방향을 통틀어 뒤집을 돌 전체를 저장할 리스트
	private List<Vector3> flipList = new List<Vector3> ();

	//추가됨. 돌을 놓을 수 있는 타일을 저장할 리스트
	private List<Vector3> availList = new List<Vector3> ();

	//추가됨. 임시 생성된 돌들을 저장할 리스트
	private List<GameObject> removalList = new List<GameObject>();

	private bool itemActiveState = false;
	private int itemCode = -1;

	//추가됨. 놓을 곳이 없어서 턴을 넘긴 플레이어를 알려주는 변수
	private bool whiteTurnSkip = false;
	private bool blackTurnSkip = false;

	//추가됨. 놓을 수 있는 타일을 한 번만 알려주도록 하는 변수
	private bool needCreate = true;

	//추가됨. 승자가 결정되는지 알려주는 변수
	private bool checkWinner = true;

	//추가됨. 놓을 수 있는 자리를 알려주는 임시 프리펩
	public GameObject removalPrefab;

	public GameObject reversiPrefab;
	public Piece[,] activedPieces{ set; get; }

	//추가됨. 승리한 플레이어를 표시하는 텍스트
	public Text resultText;

	//추가됨. WHITE_PLAYER의 돌 수
	public static int whitePieces = 2;
	//추가됨. BLACK_PLAYER의 돌 수
	public static int blackPieces = 2;

	private void Start(){
		activedPieces = new Piece[8, 8];
		initBoard ();
	}


	private float nextFire = 0.0f;
	private float fireRate = 1.8f;

	private void Update(){
		UpdateSelection ();
		DrawBoard ();
			
		//추가됨
		if(checkWinner) {
			DecideWinner();
			checkWinner = false;
		}

		//추가됨
		if (needCreate) {
			DrawAvail ();
		}
			
		if (Input.GetMouseButtonUp (0) && Time.time > nextFire) {
			nextFire = Time.time + fireRate;
			if (controllStatus == false) {
				Debug.Log ("cannot accept input");
				return;
			}
			
			startAction(selectionX, selectionY, currentPlayer);
		}
	}

	// 추가됨. 승리조건에 따른 메시지 출력
	private void DecideWinner() {
		if (whitePieces == 0) {
			resultText.text = "Black Wins!";
			needCreate = false;
			UIController.result = true;
		} else if (blackPieces == 0) {
			resultText.text = "White Wins!";
			UIController.result = true;
			needCreate = false;
		} else if (whiteTurnSkip && blackTurnSkip) {
			if (whitePieces > blackPieces) {
				resultText.text = "White Wins!";
			} else if (blackPieces > whitePieces) {
				resultText.text = "Black Wins!";
			} else {
				resultText.text = "Draw!";
			}
			UIController.result = true;
			needCreate = false;
		}
	}

	// 추가됨. 돌을 놓을수 있는 곳을 표시
	private void DrawAvail() {
		Vector3 availStone = Vector3.zero;

		availList.Clear ();

		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				if(activedPieces [i, j] != null && activedPieces [i, j].getOwner() == currentPlayer) {
					checkAvail (i, j);
				}
			}
		}

		if (availList.Count != 0) {
			if (currentPlayer == 0) {
				whiteTurnSkip = false;
			} else {
				blackTurnSkip = false;
			}

			while (availList.Count > 0) {
				availStone.x = availList [0].x;
				availStone.z = availList [0].z;

				Vector3 spawnPosition = getTileCenter ((int)availStone.x, (int)availStone.z);

				GameObject go = Instantiate (removalPrefab, spawnPosition, Quaternion.identity) as GameObject;

				removalList.Add (go);

				availList.RemoveAt (0);
			}

			needCreate = false;

		} else {
			if (currentPlayer == 0) {
				whiteTurnSkip = true;
				print ("white가 놓을 곳이 없음. black 턴으로 이동");
			} else {
				blackTurnSkip = true;
				print ("black이 놓을 곳이 없음. white 턴으로 이동");
			}
			currentPlayer = ~currentPlayer;
			needCreate = true;
			checkWinner = true;
		}
	}

	//추가됨. 돌을 놓을 수 있는 타일을 찾는 함수
	private void checkAvail(int x, int y) {
		bool enemyFound = false;
		Vector3 availStone = Vector3.zero;

		int offsetX = 0, offsetY = 0;
		int tempX = x;
		int tempY = y;
		int j = 0;

		for (int i = 0; i < 8; i++) {
			offsetX = dx [i];
			offsetY = dy [i];

			tempX += offsetX;
			tempY += offsetY;

			while (checkArrangeVaildation (tempX, tempY) == true) {
				if (activedPieces [tempX, tempY] != null && activedPieces [tempX, tempY].getOwner () == ~currentPlayer) {
					enemyFound = true;
					tempX += offsetX;
					tempY += offsetY;
				} else if (activedPieces [tempX, tempY] == null && enemyFound) {
					availStone.x = tempX;
					availStone.z = tempY;

					for (j = 0; j < availList.Count; j++) {
						if (availList [j] == availStone) {
							break;
						}
					}

					if (j == availList.Count) {
						availList.Add (availStone);
					}

					break;
				} else {
					break;
				}
			}

			tempX = x;
			tempY = y;
			enemyFound = false;
		}
	}

	//추가됨. 각 사용자의 돌 개수를 세는 함수
	private void CountPieces() {
		int white = 0, black = 0;
		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				if (activedPieces [i, j] != null) {
					if (activedPieces [i, j].getOwner() == 0) {
						white++;
					} else {
						black++;
					}
				}
			}
		}
		whitePieces = white;
		blackPieces = black;
	}


	private void UpdateSelection(){
		if (!Camera.main) {
			return;
		}
		RaycastHit hit;
		if (Physics.Raycast (
			   Camera.main.ScreenPointToRay (Input.mousePosition), 
			   out hit, 
			   25.0f,
			   LayerMask.GetMask ("BoardPlane"))) {

			selectionX = (int)hit.point.x;
			selectionY = (int)hit.point.z;
//			Debug.Log (hit.point);
		} else {
			selectionX = -1;
			selectionY = -1;
		}
	}


	private void initBoard(){
		spawnPiece (4, 3, WHITE_PLAYER);
		spawnPiece (4, 4, BLACK_PLAYER);

		spawnPiece (3, 3, BLACK_PLAYER);
		spawnPiece (3, 4, WHITE_PLAYER);
	}

	private Vector3 getTileCenter(int x, int y){
		Vector3 origin = Vector3.zero;
		origin.x += (TILE_SIZE * x) + TILE_OFFSET;
		origin.z += (TILE_SIZE * y) + TILE_OFFSET;

		return origin;
	}

	private void DrawBoard(){
		//single tile's size 1m * 8 * 8
		Vector3 widthLine = Vector3.right * 8;
		Vector3 heightLine = Vector3.forward * 8;


//		drawing checker box
		for (int i = 0; i <= 8; i++) {
			Vector3 start = Vector3.forward * i;
			Debug.DrawLine (start, start + widthLine);
			for (int j = 0; j <= 8; j++) {
				start = Vector3.right * i;
				Debug.DrawLine (start, start + heightLine);
			}
		}

		//Draw the selection
		if (selectionX >= 0 && selectionY >= 0) {
			Debug.DrawLine (
				Vector3.forward * selectionY + Vector3.right * selectionX,
				Vector3.forward * (selectionY + 1) + Vector3.right * (selectionX + 1)
			);

			Debug.DrawLine (
				Vector3.forward * (selectionY + 1) + Vector3.right * selectionX,
				Vector3.forward * selectionY + Vector3.right * (selectionX + 1)
			);
		}
	}

	private void spawnPiece(int x, int y, int player){

		Vector3 spawnPosition = getTileCenter (x, y);
		Quaternion rotationState = 
			(player == WHITE_PLAYER) ? Quaternion.identity : Quaternion.AngleAxis (180, Vector3.left);

		GameObject go = Instantiate (reversiPrefab, spawnPosition, rotationState) as GameObject;
		go.transform.SetParent (transform);

		activedPieces [x, y] = go.GetComponent<Piece> ();
		activedPieces [x, y].setPosition (x, y);
		activedPieces [x, y].setOwner (player);
	}



	public bool checkArrangeVaildation(int x, int y){
		if ((0 <= x && x < 8 ) && (0 <= y && y < 8)) {
			return true;
		} else {
			return false;
		}
	}
		
	private void startAction(int x, int y, int player){

		//추가됨
		int nextX = 0, nextY = 0;

		if (checkArrangeVaildation (x, y) == false) {
			return;
		}

		if (activedPieces [x, y] != null) {
			Debug.Log ("You can't select that area");
			return;
		} else {
			Debug.Log ("current Player : " + currentPlayer);

			checkSpawnAbility ();

			if (flipList.Count > 0) {
				controllStatus = false;

				while (removalList.Count > 0) {
					Destroy (removalList[0]);
					removalList.RemoveAt (0);
				}

				spawnPiece (x, y, currentPlayer);

				if (itemActiveState == true) {
					itemActiveState = false;
					Debug.Log ("Item code : " + itemCode); 
					switch (itemCode) {
					case 1: 
						Debug.Log ("flip activate");
						useFlipItem (x, y);
						break;
					case 2:
						useLineItem (x, y);
						break;
					default:
						break;
					}
				}

				// 추가됨. 아이템이 선택되지 않았을 경우의 일반적인 경우
				else {
					while (flipList.Count > 0) {
						nextX = (int)flipList [0].x;
						nextY = (int)flipList [0].z;
						activedPieces [nextX, nextY].flipPiece ();
						activedPieces [nextX, nextY].setOwner (currentPlayer);

						flipList.RemoveAt (0);
					}
				}
					
				CountPieces ();
				currentPlayer = ~currentPlayer;
				needCreate = true;
				checkWinner = true;
			}
		}
	}

	// 추가됨. 클릭한 타일에서 8방향의 뒤집을 돌들을 찾는 함수
	private void checkSpawnAbility() {
		bool enemyFound = false;
		Vector3 flipStone = Vector3.zero;

		int offsetX = 0, offsetY = 0;
		int tempX = selectionX;
		int tempY = selectionY;

		flipList.Clear ();

		for (int i = 0; i < 8; i++) {
			offsetX = dx [i];
			offsetY = dy [i];

			tempX += offsetX;
			tempY += offsetY;

			while (checkArrangeVaildation (tempX, tempY) == true) {
				if (activedPieces [tempX, tempY] != null && activedPieces [tempX, tempY].getOwner () == ~currentPlayer) {
					enemyFound = true;
					tempX += offsetX;
					tempY += offsetY;
				} else if (activedPieces [tempX, tempY] != null && activedPieces [tempX, tempY].getOwner () == currentPlayer && enemyFound) {
					tempX -= offsetX;
					tempY -= offsetY;
					while (tempX != selectionX || tempY != selectionY) {
						flipStone.x = tempX;
						flipStone.z = tempY;

						flipList.Add (flipStone);

						tempX -= offsetX;
						tempY -= offsetY;
					} 
					break;
				} else {
					break;
				}
			}

			tempX = selectionX;
			tempY = selectionY;
			enemyFound = false;
		}
	}
			


	public void activateItem(int itemCode){
		Debug.Log ("Item Seleceted");
		this.itemCode = itemCode;
		itemActiveState = true;
	}

	private void useFlipItem(int x, int y){
		for (int i = 0; i < 8; i++) {
			int nextX = dx [i] + x;
			int nextY = dy [i] + y;

			if (checkArrangeVaildation (nextX, nextY)) {
				if (activedPieces [nextX, nextY] != null) {
					activedPieces [nextX, nextY].flipPiece ();
					activedPieces [nextX, nextY].setOwner (currentPlayer);
				}
			}
		}
	}

	private void useLineItem(int x, int y){
		for (int i = 0; i < 8; i++) {
			if (i == x) {
				continue;
			} else {
				if (activedPieces [i, y] != null
					&& currentPlayer != activedPieces [i, y].getOwner ()) {
					activedPieces [i, y].flipPiece ();
					activedPieces [i, y].setOwner (currentPlayer);
				}
			}
		}
		for (int i = 0; i < 8; i++) {
			if (i == y) {
				continue;
			} else {
				if (activedPieces [x, i] != null
					&& currentPlayer != activedPieces [x, i].getOwner ()) {
					activedPieces [x, i].flipPiece ();
					activedPieces [x, i].setOwner (currentPlayer);
				}
			}
		}


	}

}
