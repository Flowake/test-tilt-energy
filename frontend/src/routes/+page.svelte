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

<form method="POST" use:enhance>
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
			<Input {...attrs} type="number" max="75" bind:value={$formData.total_consumption} />
		</Form.Control>
		<Form.Description>The total consumption in kWh per day of your household</Form.Description>
		<Form.FieldErrors />
	</Form.Field>
	<Form.Fieldset {form} name="appliances">
		<Form.Legend>Owned appliances</Form.Legend>
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
		<Button type="button" on:click={addAppliance}>Add Appliance</Button>
		{#each $formData.appliances as val, i}
			<Form.ElementField {form} name="appliances[{i}]">
				<Form.Control>
					<Form.Label>{appliances[val]}</Form.Label>
					<Button type="button" on:click={() => removeApplianceByIndex(i)}>Remove appliance</Button>
				</Form.Control>
				<Form.Description class="sr-only">Select the appliances you own</Form.Description>
				<Form.FieldErrors />
			</Form.ElementField>
		{/each}
		<Form.FieldErrors />
	</Form.Fieldset>
	<Button type="submit">Submit</Button>
</form>
