<script lang="ts">
	import { Label } from '$lib/components/ui/label/index.js';
	import { appliances } from '$lib/schema';
	export let data;

	const totalApplianceConsumption: number = Object.values(data.consumption_per_appliance).reduce(
		(acc, value) => acc + value,
		0
	);
</script>

<div class="mx-auto flex min-h-screen max-w-2xl flex-col items-center justify-center">
	<img
		src="https://framerusercontent.com/images/1rbwaKSHRr8O2nfFYEdpg3SLtXc.png"
		alt="Company Logo"
		class="mb-4 h-32"
	/>
	<h1 class="scroll-m-20 text-4xl font-extrabold tracking-tight lg:text-5xl">
		Consumption Calculator
	</h1>
	<p class="mb-4 leading-7 [&:not(:first-child)]:mt-6">
		Based on your appliances and on your provided total consumption of {data.total_consumption} kWh,
		we estimated the individual appliances consumption.
	</p>

	<div class="items-left mx-auto flex w-full flex-col justify-center">
		<h2
			class="scroll-m-20 border-b pb-2 text-3xl font-semibold tracking-tight transition-colors first:mt-0"
		>
			Results
		</h2>
		<p class="leading-7 [&:not(:first-child)]:mt-6">
			This is our closest estimation, which adds up to a consumption of {Math.round(
				totalApplianceConsumption / 100
			) / 10} kWh.
		</p>

		<div class="my-6 w-full overflow-y-auto">
			<table class="w-full">
				<thead>
					<tr class="m-0 border-t p-0 even:bg-muted">
						<th
							class="border px-4 py-2 text-left font-bold [&[align=center]]:text-center [&[align=right]]:text-right"
						>
							Appliance
						</th>
						<th
							class="border px-4 py-2 text-left font-bold [&[align=center]]:text-center [&[align=right]]:text-right"
						>
							Consumption (kWh)
						</th>
					</tr>
				</thead>
				<tbody>
					{#each Object.entries(data.consumption_per_appliance) as [appliance, consumption]}
						<tr class="m-0 border-t p-0 even:bg-muted">
							<td
								class="border px-4 py-2 text-left [&[align=center]]:text-center [&[align=right]]:text-right"
							>
								{appliances[appliance]}
							</td>
							<td
								class="border px-4 py-2 text-left [&[align=center]]:text-center [&[align=right]]:text-right"
							>
								{Math.round(consumption / 100) / 10}
							</td>
						</tr>
					{/each}
				</tbody>
			</table>
		</div>
	</div>
</div>
