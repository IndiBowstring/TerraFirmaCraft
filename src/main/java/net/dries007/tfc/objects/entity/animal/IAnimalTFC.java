/*
 * Work under Copyright. Licensed under the EUPL.
 * See the project README.md and LICENSE.txt for more information.
 */

package net.dries007.tfc.objects.entity.animal;

import java.util.Collections;
import java.util.List;
import javax.annotation.Nonnull;

import net.minecraft.item.ItemStack;
import net.minecraft.world.biome.Biome;

import net.dries007.tfc.util.OreDictionaryHelper;
import net.dries007.tfc.util.calendar.CalendarTFC;

public interface IAnimalTFC
{
    /**
     * Check if this animal can spawn in said conditions
     *
     * @param biome       the biome in chunk that is trying to spawn this animal
     * @param temperature the average temperature of this region
     * @param rainfall    the average rainfall of this region
     * @return true if this animal can be spawn in this conditions
     */
    boolean isValidSpawnConditions(Biome biome, float temperature, float rainfall);

    /**
     * Get this animal gender, female or male
     *
     * @return Gender of this animal
     */
    Gender getGender();

    /**
     * Set this animal gender, used on spawn/birth
     *
     * @param gender the Gender to set to
     */
    void setGender(Gender gender);

    /**
     * Returns the birth day of this animal. Determines how old this animal is
     *
     * @return returns the day this animal has been birth
     */
    int getBirthDay();

    /**
     * Sets the birth day of this animal. Used to determine how old this animal is
     *
     * @param value the day this animal has been birth. Used when this animal spawns.
     */
    void setBirthDay(int value);

    /**
     * Returns the familiarity of this animal
     *
     * @return float value between 0-1.
     */
    float getFamiliarity();

    /**
     * Set this animal familiarity
     *
     * @param value float value between 0-1.
     */
    void setFamiliarity(float value);

    /**
     * Returns true if this female is pregnant, or the next time it ovulates, eggs are fertilized.
     *
     * @return true if this female has been fertilized.
     */
    boolean isFertilized();

    /**
     * Set if this female is fertilized
     *
     * @param value true on fertilization (mating)
     */
    void setFertilized(boolean value);

    /**
     * Event: Do things on fertilization of females (ie: save the male genes for some sort of genetic selection)
     */
    default void onFertilized(@Nonnull IAnimalTFC male)
    {
        setFertilized(true);
    }

    /**
     * Used by model renderer to scale the size of the animal
     *
     * @return double value between 0(birthday) to 1(full grown adult)
     */
    default double getPercentToAdulthood()
    {
        double value = (CalendarTFC.PLAYER_TIME.getTotalDays() - this.getBirthDay()) / (double) getDaysToAdulthood();
        if (value > 1) value = 1;
        if (value < 0) value = 0;
        return value;
    }

    /**
     * Get this entity age, based on birth
     *
     * @return the Age enum of this entity
     */
    default Age getAge()
    {
        // Old Age isn't being used for the time being
        return CalendarTFC.PLAYER_TIME.getTotalDays() >= this.getBirthDay() + getDaysToAdulthood() ? Age.ADULT : Age.CHILD;
    }

    /**
     * Get the number of days needed for this animal to be adult
     *
     * @return number of days
     */
    int getDaysToAdulthood();

    /**
     * Check if this animal is ready to mate
     *
     * @return true if ready
     */
    default boolean isReadyToMate()
    {
        return this.getAge() == Age.ADULT && !(this.getFamiliarity() < 0.3f) && !this.isFertilized() && !this.isHungry();
    }

    /**
     * Check if said item can feed this animal
     *
     * @param stack the itemstack to check
     * @return true if item is used to feed this animal (entice and increase familiarity)
     */
    default boolean isFood(@Nonnull ItemStack stack)
    {
        return OreDictionaryHelper.doesStackMatchOre(stack, "grain");
    }

    /**
     * Is this animal hungry?
     *
     * @return true if this animal can be fed by player
     */
    boolean isHungry();

    /**
     * Which animal type is this? Do this animal lay eggs or give birth to it's offspring?
     *
     * @return the enum Type of this animal.
     */
    Type getType();

    /**
     * Some animals can give products (eg: Milk, Wool and Eggs)
     * This function returns if said animal is ready to be worked upon
     * (or if it is ready to lay eggs on it's own)
     *
     * @return true if it is ready for product production
     */
    default boolean isReadyForAnimalProduct()
    {
        return false;
    }

    /**
     * Get the products of this animal
     * Can return more than one item itemstack
     * fortune and other behaviour should not be handled here
     * Suggestion: EntityLiving#processInteract() for right clicking handling
     *
     * @return a list of itemstack
     */
    default List<ItemStack> getProducts()
    {
        return Collections.emptyList();
    }

    enum Age
    {
        CHILD, ADULT, OLD
    }

    enum Gender
    {
        MALE, FEMALE;

        public static Gender fromBool(boolean value)
        {
            return value ? MALE : FEMALE;
        }

        public boolean toBool()
        {
            return this == MALE;
        }
    }

    enum Type
    {
        MAMMAL, OVIPAROUS
    }
}
