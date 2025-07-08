from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class Category(models.Model):
    CATEGORIE_NAME = [
        ("Antibiotics", "Antibiotics"),
        ("Painkillers", "Painkillers"),
        ("Antivirals", "Antivirals"),
        ("Antifungals", "Antifungals"),
        ("Antiparasitics", "Antiparasitics"),
        ("Antipyretics", "Antipyretics"),
        ("Antidepressants", "Antidepressants"),
        ("Antipsychotics", "Antipsychotics"),
        ("Antiepileptics", "Antiepileptics"),
        ("Antimalarials", "Antimalarials"),
        ("Anthelmintics", "Anthelmintics"),
        ("Antibacterial", "Antibacterial"),
        ("Antiviral", "Antiviral"),
        ("Antifungal", "Antifungal"),
        ("Antiparasitic", "Antiparasitic"),
        ("Antipyretic", "Antipyretic"),
        ("Antidepressant", "Antidepressant"),
        ("Antipsychotic", "Antipsychotic"),
        ("Antiepileptic", "Antiepileptic"),
        ("Antimalarial", "Antimalarial"),
        ("Anthelmintic", "Anthelmintic"),
        ("Autres", "Autres"),
    ]
    name = models.CharField(max_length=100, choices=CATEGORIE_NAME)
    description = models.TextField(_("Description"), blank=True, null=True)
    
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
    
    def __str__(self):
        return self.name

class Medication(models.Model):
    name = models.CharField(_("Medication Name"), max_length=200)
    description = models.TextField(_("Description"))
    price = models.DecimalField(_("Price"), max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(_("Stock Quantity"))
    expiry_date = models.DateField(_("Expiry Date"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="medications")
    image = models.ImageField(_("Image"), upload_to="medications/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Medication")
        verbose_name_plural = _("Medications")
    
    def __str__(self):
        return self.name

class Purchase(models.Model):
    PAYMENT_CHOICES = (
        ('cash', _('Cash')),
        ('card', _('Card')),
        ('mobile', _('Mobile Payment')),
    )
    
    customer_name = models.CharField(_("Customer Name"), max_length=200)
    customer_phone = models.CharField(_("Customer Phone"), max_length=20, blank=True, null=True)
    total_amount = models.DecimalField(_("Total Amount"), max_digits=10, decimal_places=2)
    payment_method = models.CharField(_("Payment Method"), max_length=20, choices=PAYMENT_CHOICES, default='cash')
    staff = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="purchases")
    purchase_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _("Purchase")
        verbose_name_plural = _("Purchases")
    
    def __str__(self):
        return f"Purchase #{self.id} - {self.customer_name}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE, related_name="items")
    medication = models.ForeignKey(Medication, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(_("Quantity"))
    unit_price = models.DecimalField(_("Unit Price"), max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(_("Subtotal"), max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = _("Purchase Item")
        verbose_name_plural = _("Purchase Items")
    
    def __str__(self):
        return f"{self.medication.name} ({self.quantity})"
    
    def save(self, *args, **kwargs):
        self.subtotal = self.quantity * self.unit_price
        super().save(*args, **kwargs)

class Medicament(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    dosage = models.CharField(max_length=100, blank=True, null=True)
    forme = models.CharField(max_length=100, blank=True, null=True)  # comprimé, gélule, sirop, etc.
    laboratoire = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='medicaments/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.nom

