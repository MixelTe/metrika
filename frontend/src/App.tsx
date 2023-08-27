import { Navigate, Route, Routes, matchPath, useLocation, useParams } from "react-router-dom";
import useUser from "./api/user";
import hasPermission, { Operation } from "./api/operations";
import Spinner from "./components/Spinner";
import ScrollToTop from "./utils/scrollToTop";

import NotFoundPage from "./pages/NotFoundPage";
import NoPermissionPage from "./pages/NoPermissionPage";
import AuthPage from "./pages/AuthPage";
import IndexPage from "./pages/IndexPage";
import AppPage from "./pages/AppPage";


export default function App()
{
	const user = useUser();
    const { pathname } = useLocation()
	const getParam = (path: string, param: string | number) => matchPath(path, pathname)?.params[param] || "";

	function ProtectedRoute(permission: Operation | null, path: string, element: JSX.Element)
	{
		return <Route path={path} element={
			!user.data?.auth ? <Navigate to="/auth" /> : (
				permission == null || hasPermission(user,
					typeof permission == "string" ? permission : [permission[0], getParam(path, permission[1])]
				) ? element : <NoPermissionPage />
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
				{ProtectedRoute(["view_app", "appId"], "/app/:appId", <AppPage />)}
				{ProtectedRoute(null, "*", <NotFoundPage />)}
			</Routes>
		}
	</div>
}
