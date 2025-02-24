##### 1.Candidate一覧が空であることを確認
|Method|Request URL|Code|
|--|--|--|
|GET|http://localhost:8000/candidates|200|

##### Request body
なし

##### Response body
```json
[]
```
---
##### 2.Candidateを作成
|Method|Request URL|Code|
|--|--|--|
|POST|http://localhost:8000/candidates|200|

##### Request body
```json
{
  "id": 0,
  "name": "田中 太郎",
  "party": "自民党",
  "win_count": 10
}
```

##### Response body
```json
{
  "message": "Candidate Created Successfully."
}
```
---
##### 3.DistrictVoteを作成
|Method|Request URL|Code|
|--|--|--|
|POST|http://localhost:8000/district_vote|200|

##### Request body
```json
{
  "candidate_id": 0,
  "prefecture": "大阪府",
  "district": "3",
  "votes": 123
}
```

##### Response body
```json
{
  "message": "District Vote Created Successfully."
}
```
---
##### 4.議員情報と小選挙区情報をまとめて取得
|Method|Request URL|Code|
|--|--|--|
|GET|http://localhost:8000/candidates/0|200|

##### Request body
なし

##### Response body
```json
{
  "id": 0,
  "name": "田中 太郎",
  "party": "自民党",
  "win_count": 10,
  "prefecture": "大阪府",
  "district": 3,
  "votes": 123
}
```