<script lang="ts">
	import { superForm } from 'sveltekit-superforms';
	import { zodClient } from 'sveltekit-superforms/adapters';
	import * as Select from '$lib/components/ui/select/index.js';
	import type { PageData } from './$types.js';
	import { schema, appliances, type Appliances } from '$lib/schema';
	import * as Form from '$lib/components/ui/form/index.js';
	import { Input } from '$lib/components/ui/input/index.js';
	import { Button } from '$lib/components/ui/button/index.js';

	export let data: PageData;

	let applianceSelect: Appliances;

	function removeApplianceByIndex(index: number) {
		$formData.appliances = $formData.appliances.filter((_, i) => i !== index);
	}

	function addAppliance() {
		$formData.appliances = [...$formData.appliances, applianceSelect.value];
	}

	const form = superForm(data.form, {
		validators: zodClient(schema),
		dataType: 'json'
	});
	const { form: formData, enhance } = form;
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
	<p class="leading-7 [&:not(:first-child)]:mt-6">
		Compute the individual consumption of your appliances by providing the appliances you own and
		the total consumption of your household.
	</p>
	<form method="POST" use:enhance class="w-full rounded border border-gray-300 p-4">
		<Form.Field {form} name="email">
			<Form.Control let:attrs>
				<Form.Label>Email</Form.Label>
				<Input {...attrs} type="email" bind:value={$formData.email} />
			</Form.Control>
			<Form.FieldErrors />
		</Form.Field>
		<Form.Field {form} name="total_consumption">
			<Form.Control let:attrs>
				<Form.Label>Total consumption (kWh)</Form.Label>
				<Input {...attrs} type="number" min="0" max="75" bind:value={$formData.total_consumption} />
			</Form.Control>
			<Form.Description>The total consumption in kWh per day of your household</Form.Description>
			<Form.FieldErrors />
		</Form.Field>
		<Form.Fieldset {form} name="appliances">
			<Form.Legend>Owned appliances</Form.Legend>
			<div class="flex items-center">
				<Select.Root
					selected={applianceSelect}
					onSelectedChange={(s) => {
						applianceSelect = s;
					}}
				>
					<Select.Trigger>
						<Select.Value placeholder="Select an appliance" />
					</Select.Trigger>
					<Select.Content>
						{#each Object.entries(appliances) as [value, label]}
							<Select.Item {value} {label} />
						{/each}
					</Select.Content>
				</Select.Root>
				<Button variant="secondary" class="ml-4" on:click={addAppliance}>Add Appliance</Button>
			</div>
			<Form.Description>Select the appliances you own</Form.Description>
			{#each $formData.appliances as val, i}
				<Form.ElementField {form} name="appliances[{i}]">
					<Form.Control>
						<div class="mb-1 flex w-full flex-row items-center justify-between">
							<Form.Label class=" mx-1 w-full rounded border border-gray-300 p-3 text-center"
								>{appliances[val]}</Form.Label
							>
							<Form.Button variant="destructive" on:click={() => removeApplianceByIndex(i)}
								>Remove</Form.Button
							>
						</div>
					</Form.Control>
					<Form.FieldErrors />
				</Form.ElementField>
			{/each}
			<Form.FieldErrors />
		</Form.Fieldset>
		<div class="justify-left flex items-center">
			<Form.Button type="submit" class="mb-4">Get the results</Form.Button>
		</div>
	</form>
</div>
