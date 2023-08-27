import { UseQueryResult } from "react-query";
import useUser, { User } from "./user";

const Operations = {
	view_app: "view_app",
	add_app: "add_app",
	edit_app: "edit_app",
}

export type Operation = AllOperations | [AllOperations, ObjectId];
type AllOperations = keyof typeof Operations;
type ObjectId = string | number;

export default function hasPermission(user: UseQueryResult<User, unknown>, operation: Operation)
{
	return !!(user.data?.auth && user.data?.operations.includes(operationToString(operation)));
}

export function useHasPermission(operation: Operation)
{
	const user = useUser();
	return !!(user.data?.auth && user.data?.operations.includes(operationToString(operation)));
}

function operationToString(operation: Operation)
{
	if (typeof operation == "string")
		return operation
	return operation[0] + "-" + operation[1]
}
