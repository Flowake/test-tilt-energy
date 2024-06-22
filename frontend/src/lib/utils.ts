export function formatApplianceName(name: string) {
	return name
		.split('_')
		.map((word) => word.charAt(0).toUpperCase() + word.slice(1))
		.join(' ');
}
