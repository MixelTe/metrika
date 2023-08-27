import { UseQueryResult } from "react-query";
import useUser, { User } from "./user";

const Operations = {
	view_app: "view_app",
	add_app: "add_app",
	edit_app: "edit_app",
}

export type Operation = keyof typeof Operations;

export default function hasPermission(user: UseQueryResult<User, unknown>, operation: Operation)
{
	return !!(user.data?.auth && user.data?.operations.includes(operation));
}

export function useHasPermission(operation: Operation)
{
	const user = useUser();
	return !!(user.data?.auth && user.data?.operations.includes(operation));
}
