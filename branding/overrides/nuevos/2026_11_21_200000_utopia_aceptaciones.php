<?php

// Utopia Tickets (nov-2026). Fichero NUEVO que añade la marca (no sustituye nada de la imagen): registro de la aceptación de
// las condiciones en el alta libre de promotores y de la revisión de cada alta por Utopia. Idempotente.

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        if (! Schema::hasTable('utopia_aceptaciones')) {
            Schema::create('utopia_aceptaciones', function (Blueprint $table) {
                $table->id();
                $table->unsignedBigInteger('account_id')->index();
                $table->unsignedBigInteger('user_id')->nullable();
                $table->string('email');
                $table->string('documento', 50);
                $table->string('version', 50);
                $table->string('sha256', 64)->nullable();
                $table->string('url', 255)->nullable();
                $table->string('origen', 30)->default('registro');
                $table->string('ip', 64)->nullable();
                $table->string('user_agent', 500)->nullable();
                $table->timestamp('aceptado_en');
                $table->timestamp('created_at')->nullable();
            });
        }

        if (! Schema::hasTable('utopia_revisiones_altas')) {
            Schema::create('utopia_revisiones_altas', function (Blueprint $table) {
                $table->id();
                $table->unsignedBigInteger('account_id')->index();
                $table->string('resultado', 30);
                $table->text('nota')->nullable();
                $table->string('revisado_por', 100);
                $table->timestamp('revisado_en');
            });
        }
    }

    public function down(): void
    {
        Schema::dropIfExists('utopia_revisiones_altas');
        Schema::dropIfExists('utopia_aceptaciones');
    }
};
