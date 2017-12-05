using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BoardManager : MonoBehaviour {
	//	public static bool controllStatus = true;
	private const string SERVER_URL = "http://18.217.70.204:5090/post";
	// private const string SERVER_URL = "http://0.0.0.0:5090/post";
	private bool AIMODE = true;
	bool serverAiActionRequestResult = false;

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

	public Image image1;
	public Image image2;
	public Text text1;
	public Text text2;
	public Vector2 vector1 = new Vector2(60, 60);
	public Vector2 vector2 = new Vector2(40, 40);

	private void Start(){
		activedPieces = new Piece[8, 8];
		initBoard ();
		currentPlayer = BLACK_PLAYER;
	}


	public static float nextFire = 0.0f;
	private float fireRate = 1.8f;

	private void Update(){
		checkPause ();
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

			//	DrawAvail
			//	1. check is there any skiped turn
			//	2. count and draw avail position marker(red obj)
			//	3. if DrawAvail is called, needCreate return to fail;
		}
	
		activateCurrentTurn ();
	}

	private void activateCurrentTurn(){

		if (AIMODE == true) {
			//serverAiActionRequestResult rename to  => serverReqeustState
			if (serverAiActionRequestResult == false && currentPlayer == WHITE_PLAYER) {
				sendAiRequest ();
			} else if (currentPlayer == BLACK_PLAYER) {
				serverAiActionRequestResult = false;
				getUserInput ();
			}
		} else if (AIMODE == false) {
			getUserInput ();
		}
	}


	private void getUserInput(){
		if (Input.GetMouseButtonUp (0) && Time.time > nextFire) {
			nextFire = Time.time + fireRate;
			startAction (selectionX, selectionY, currentPlayer);
		}
	}

	IEnumerator noticeTo(int player){
		//StartCoroutine(noticePlayersTurn(player);	
		//do action;
		resultText.text = "No place to select!\nPass to next player";
		resultText.enabled = true;
		yield return new WaitForSeconds (1.0f);
		resultText.enabled = false;

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

				Vector3 spawnPosition = getTileCenter ((int)availStone.x, (int)(availStone.z));
				spawnPosition.Set ((float)(spawnPosition.x), (float)spawnPosition.y,(float)(spawnPosition.z - 0.25));

				GameObject go = Instantiate (removalPrefab, spawnPosition, Quaternion.AngleAxis(180, Vector3.up)) as GameObject;

				removalList.Add (go);

				availList.RemoveAt (0);
			}

			needCreate = false;

		} else {
			if (currentPlayer == 0) {
				whiteTurnSkip = true;
				print ("white가 놓을 곳이 없음. black 턴으로 이동");
				StartCoroutine(noticeTo(currentPlayer));
			} else {
				blackTurnSkip = true;
				print ("black이 놓을 곳이 없음. white 턴으로 이동");
				StartCoroutine(noticeTo(currentPlayer));
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
					if (activedPieces [i, j].getOwner() == WHITE_PLAYER) {
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
		spawnPiece (4, 3, BLACK_PLAYER);
		spawnPiece (4, 4, WHITE_PLAYER);

		spawnPiece (3, 3, WHITE_PLAYER);
		spawnPiece (3, 4, BLACK_PLAYER);
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
			//			Debug.Log (selectionX + ", " + selectionY);
		}
	}

	private void spawnPiece(int x, int y, int player){

		Vector3 spawnPosition = getTileCenter (x, y);
		Quaternion rotationState =
			(player == BLACK_PLAYER) ? Quaternion.AngleAxis(180, Vector3.up) : Quaternion.AngleAxis (180, Vector3.left);

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
		int nextX = 0, nextY = 0;

		if (checkArrangeVaildation (x, y) == false) {
			return;
		}

		if (activedPieces [x, y] != null) {
			Debug.Log ("You can't select that position");
			return;
		} else {
			checkSpawnAbility (x, y);

			if (currentPlayer == BLACK_PLAYER) {
				Debug.Log ("flip count : " + flipList.Count);
				Debug.Log ("x : " + x + ", y: " + y);
			}

			if (flipList.Count > 0) {
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
				} else {
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
	private void checkSpawnAbility(int xCoords, int yCoords) {
		bool enemyFound = false;
		Vector3 flipStone = Vector3.zero;

		int offsetX = 0, offsetY = 0;
		int tempX = xCoords;
		int tempY = yCoords;

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
					while (tempX != xCoords || tempY != yCoords) {
						if (currentPlayer == BLACK_PLAYER) {
							Debug.Log ("founded!!!");
						}
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

			tempX = xCoords;
			tempY = yCoords;
			enemyFound = false;
		}
	}



	public void setPlayerTurnUI(int currentPlayer) {
			if (currentPlayer == BLACK_PLAYER) {
				text1.fontSize = 50;
				text1.color = Color.red;
				text2.fontSize = 30;
				text2.color = Color.black;

				image1.rectTransform.sizeDelta = vector1;
				image2.rectTransform.sizeDelta = vector2;
			} else {
				text1.fontSize = 30;
				text1.color = Color.black;
				text2.fontSize = 50;
				text2.color = Color.red;
				image1.rectTransform.sizeDelta = vector2;
				image2.rectTransform.sizeDelta = vector1;
			}
	}



	public void activateItem(int itemCode){
		nextFire = Time.time;
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
					activedPieces [nextX, nextY].setOwner (~activedPieces[nextX, nextY].getOwner());
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

	public static bool pauseFlag = false;

	public void checkPause(){
		if (pauseFlag) {
			Time.timeScale = 0;
		} else {
			Time.timeScale = 1;
		}
	}



	public void sendAiRequest(){
		WWWForm form = new WWWForm();
		form.AddField("status", getBoardStatus());
		form.AddField ("target", getAvailPosition ());
		WWW www = new WWW (SERVER_URL, form);
		StartCoroutine(WaitForRequest(www));
	}
		
	IEnumerator WaitForRequest(WWW www)
	{
		serverAiActionRequestResult = true;
		yield return www;
		if (www.error == null)
		{
			Pair<int, int> coords = convertOneD2TwoD(int.Parse(www.text));

			Debug.Log("result from server : " + www.text);
			// Fire AI action after 3 sec.
			yield return new WaitForSeconds(3);
			startAction (coords.First, 7 - coords.Second, currentPlayer);
			serverAiActionRequestResult = false;
			nextFire = Time.time + fireRate;
		} else {
			// Something wrong!
			Debug.Log ("WWW error: " + www.error);
			serverAiActionRequestResult = false;
		}
	}

	private string getBoardStatus(){
		string boardStatus = "";
		for (int row = 7; row >= 0; row--) {
			for (int col = 0; col < 8; col++) {
				Piece currentPiece = activedPieces [col, row];

				if (currentPiece == null) {
					boardStatus += 0;
				} else if (currentPiece.getOwner() == WHITE_PLAYER) {
					boardStatus += 2;
				} else if(currentPiece.getOwner() == BLACK_PLAYER){
					boardStatus += 1;
				}
			}
		}
		return boardStatus;
	}

	private string getAvailPosition(){
		string availPos = "";
		availList.Clear ();

		for (int i = 0; i < 8; i++) {
			for (int j = 0; j < 8; j++) {
				if(activedPieces [i, j] != null && activedPieces [i, j].getOwner() == currentPlayer) {
					checkAvail (i, j);
				}
			}
		}

		//		Debug.Log (availList.Count);
		while(availList.Count != 0){
			int xCoord = (int) availList [0].x;
			int yCoord = (int) availList [0].z;
			availPos += (convertTwoD2OneD(new Pair<int, int>(xCoord, yCoord)) + ",");
			availList.RemoveAt (0);
		}

		return availPos;
	}

	private Pair<int, int> convertOneD2TwoD(int posValue){
		int posVal = posValue;
		int yCoord = posVal / 8;
		int xCoord = posVal % 8;
		return new Pair<int,int> (xCoord, yCoord);
	}

	private int convertTwoD2OneD(Pair<int, int> coords){
		return coords.First + ((8 - (coords.Second+1)) * 8);
	}
}

public class Pair<T, U> {
	public Pair() {
	}

	public Pair(T first, U second) {
		this.First = first;
		this.Second = second;
	}


	public T First { get; set; }
	public U Second { get; set; }
};
