import { Navigate, Route, Routes } from "react-router-dom";
import useUser from "./api/user";
import hasPermission, { Operation } from "./api/operations";
import Spinner from "./components/Spinner";
import ScrollToTop from "./utils/scrollToTop";

import NotFoundPage from "./pages/NotFoundPage";
import NoPermissionPage from "./pages/NoPermissionPage";
import AuthPage from "./pages/AuthPage";
import IndexPage from "./pages/IndexPage";


export default function App()
{
	const user = useUser();

	function ProtectedRoute(permission: Operation | null, path: string, element: JSX.Element)
	{
		return <Route path={path} element={
			!user.data?.auth ? <Navigate to="/auth" /> : (
				permission == null || hasPermission(user, permission) ? element : <NoPermissionPage />
			)
		} />
	}

	return <div className="root">
		<ScrollToTop />

		{user.isLoading && <Spinner />}
		{user.isError && "Ошибка"}
		{user.isSuccess &&
			<Routes>
				<Route path="/auth" element={!user.data?.auth ? <AuthPage /> : <Navigate to="/" />} />
				{ProtectedRoute(null, "/", <IndexPage />)}
				{ProtectedRoute(null, "*", <NotFoundPage />)}
			</Routes>
		}
	</div>
}
