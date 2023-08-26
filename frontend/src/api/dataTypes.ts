export interface ResponseMsg
{
	msg: string,
}

export interface User
{
	auth: boolean,
	id: number,
	name: string,
	login: string,
	operations: string[],
}
