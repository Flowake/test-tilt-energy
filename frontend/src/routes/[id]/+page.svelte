<script lang="ts">
	import { formatApplianceName } from '$lib/utils';
	export let data;

	const totalApplianceConsumption: number = Object.values(data.consumption_per_appliance).reduce(
		(acc, value) => acc + value,
		0
	);
</script>

<div>
	<h2>Total Consumption: {data.total_consumption} kWh</h2>
	<h2>Total estimated consumption: {totalApplianceConsumption / 1000} kWh</h2>
	<h3>Consumption per appliance:</h3>
	<ul>
		{#each Object.entries(data.consumption_per_appliance) as [appliance, consumption]}
			<li>{formatApplianceName(appliance)}: {consumption / 1000} kWh</li>
		{/each}
	</ul>
</div>
