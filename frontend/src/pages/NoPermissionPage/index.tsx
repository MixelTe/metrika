import HeaderBack from "../../components/HeaderBack";
import Layout from "../../components/Layout";
import { useTitle } from "../../utils/useTtile";

export default function NoPermissionPage()
{
	useTitle("403");
	return (
		<Layout centered header={<HeaderBack />}>
			У вас недостатточно прав на просмотр этой страницы
		</Layout>
	);
}
