import HeaderBack from "../../components/HeaderBack";
import Layout from "../../components/Layout";
import { useTitle } from "../../utils/useTtile";

export default function NotFoundPage()
{
	useTitle("404");
	return (
		<Layout centered header={<HeaderBack />}>
			Такой страницы нет
		</Layout>
	);
}
